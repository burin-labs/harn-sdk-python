"""Render Python declarations from the closed Harn wire algebra."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from pydantic import BaseModel

from .names import Symbol, allocate
from .request import CodegenIr, WireType

RESERVED = frozenset(
    {
        "Annotated",
        "BeforeValidator",
        "WrapValidator",
        "ConfigDict",
        "ClassVar",
        "Field",
        "Literal",
        "Union",
        "TypeAliasType",
        "TypeAlias",
        "StrictStr",
        "StrictBool",
        "StrictInt",
        "StrictFloat",
        "WireModel",
        "WireValueModel",
        "WireBytes",
        "WireDecimal",
        "WireSet",
        "MISSING",
        "strict_literal",
        "wire_literal_validator",
        "wire_tuple_validator",
        "wire_value_depth",
        "ApplicationFailure",
        "Client",
        "AsyncClient",
        "SyncHandlers",
        "AsyncHandlers",
        "Server",
        "AsyncServer",
        "Protocol",
        "TypedDict",
        "Awaitable",
        "JsonValue",
        "TypeAdapter",
        "HarnClient",
        "AsyncHarnClient",
        "McpClient",
        "AsyncMcpClient",
        "NativeServer",
        "CATALOG_DIGEST",
        "BINDING_DIGEST",
        "IR_DIGEST",
        "MCP_TOOLS",
        "create_server",
        "create_async_server",
        "require_handlers",
        "bind_sync",
        "bind_async",
        "encode_wire",
        "decode_result",
        "list",
        "dict",
        "tuple",
        "str",
        "int",
        "float",
        "bool",
        "bytes",
        "set",
        "globals",
    }
)


class GenerationError(ValueError):
    def __init__(self, code: str, wire: WireType) -> None:
        self.code = code
        self.type_id = wire.id
        self.source = wire.source
        super().__init__(f"{code}: type {wire.id}")


@dataclass(frozen=True)
class Declaration:
    content: str
    source: BaseModel


def variant_identity(type_id: str, variant_id: str) -> str:
    return json.dumps(["variant", type_id, variant_id], separators=(",", ":"))


class TypeRenderer:
    def __init__(self, ir: CodegenIr) -> None:
        self.ir = ir
        self.types = {wire.id: wire for wire in ir.types}
        symbols = []
        for wire in ir.types:
            nominal = getattr(wire.shape, "nominal", None)
            declaration = getattr(wire.shape, "declaration", None)
            name = wire.name or (nominal.name if nominal is not None else None)
            name = name or (declaration.name if declaration is not None else None)
            if not name:
                input_operation = next(
                    (
                        operation
                        for operation in sorted(
                            ir.operations, key=lambda operation: operation.id
                        )
                        if operation.input == wire.id
                    ),
                    None,
                )
                if input_operation is not None:
                    name = (
                        input_operation.name[:1].upper()
                        + input_operation.name[1:]
                        + "Input"
                    )
            name = name or "Type_" + hashlib.sha256(wire.id.encode()).hexdigest()[:16]
            symbols.append(Symbol(wire.id, name))
            if wire.shape.kind == "enum":
                symbols.extend(
                    Symbol(
                        variant_identity(wire.id, variant.id), name + "_" + variant.name
                    )
                    for variant in wire.shape.variants
                )
        self.names = allocate(symbols, reserved=RESERVED)

    def reference(self, identity: str, *, quoted: bool = False) -> str:
        name = self.names[identity]
        return repr(name) if quoted else name

    def declarations(self) -> list[Declaration]:
        result = []
        ordered = sorted(self.ir.types, key=lambda entry: entry.id)
        for wire in ordered:
            if wire.shape.kind == "alias":
                continue
            result.extend(self.declare(wire))
        pending = {wire.id: wire for wire in ordered if wire.shape.kind == "alias"}
        while pending:
            ready = [
                wire
                for wire in pending.values()
                if wire.shape.kind == "alias" and wire.shape.target not in pending
            ]
            if not ready:
                raise GenerationError(
                    "invalid_alias_cycle", next(iter(pending.values()))
                )
            for wire in ready:
                result.extend(self.declare(wire))
                del pending[wire.id]
        return result

    def alias(
        self, wire: WireType, expression: str, *, depth: bool = True
    ) -> Declaration:
        name = self.reference(wire.id)
        if depth:
            expression = f"Annotated[{expression}, WrapValidator(wire_value_depth)]"
        return Declaration(
            f"{name} = TypeAliasType({name!r}, {expression})\n", wire.source
        )

    def declare(self, wire: WireType) -> list[Declaration]:
        shape = wire.shape
        if shape.kind == "null":
            return [self.alias(wire, "None")]
        if shape.kind == "boolean":
            return [self.alias(wire, "StrictBool")]
        if shape.kind == "integer":
            if shape.encoding != "json_number":
                raise GenerationError("unsupported_wire_encoding", wire)
            return [
                self.alias(
                    wire,
                    f"Annotated[StrictInt, Field(ge={int(shape.minimum)}, le={int(shape.maximum)})]",
                )
            ]
        if shape.kind == "float":
            return [
                self.alias(wire, "Annotated[StrictFloat, Field(allow_inf_nan=False)]")
            ]
        if shape.kind == "string":
            return [self.alias(wire, "StrictStr")]
        if shape.kind == "bytes":
            if shape.encoding != "base64_envelope":
                raise GenerationError("unsupported_wire_encoding", wire)
            return [self.alias(wire, "WireBytes")]
        if shape.kind == "decimal":
            if shape.encoding != "canonical_string":
                raise GenerationError("unsupported_wire_encoding", wire)
            return [self.alias(wire, "WireDecimal")]
        if shape.kind == "literal":
            value = shape.value
            if value.kind == "float":
                number = float(value.value)
                expression = f"Annotated[StrictFloat, Field(ge={number!r}, le={number!r}, allow_inf_nan=False), BeforeValidator(wire_literal_validator({number!r}))]"
            else:
                literal = (
                    None
                    if value.kind == "null"
                    else int(value.value)
                    if value.kind == "integer"
                    else value.value
                )
                expression = f"Annotated[Literal[{literal!r}], BeforeValidator(wire_literal_validator({literal!r}))]"
            return [self.alias(wire, expression)]
        if shape.kind == "list":
            return [
                self.alias(wire, f"list[{self.reference(shape.item, quoted=True)}]")
            ]
        if shape.kind == "set":
            return [
                self.alias(wire, f"WireSet[{self.reference(shape.item, quoted=True)}]")
            ]
        if shape.kind == "tuple":
            items = (
                ", ".join(self.reference(item, quoted=True) for item in shape.items)
                or "()"
            )
            return [
                self.alias(
                    wire,
                    f"Annotated[tuple[{items}], BeforeValidator(wire_tuple_validator)]",
                )
            ]
        if shape.kind == "map":
            return [
                self.alias(
                    wire, f"dict[str, {self.reference(shape.value, quoted=True)}]"
                )
            ]
        if shape.kind == "alias":
            return [
                Declaration(
                    f"{self.reference(wire.id)}: TypeAlias = {self.reference(shape.target)}\n",
                    wire.source,
                )
            ]
        if shape.kind == "union":
            members = ", ".join(
                self.reference(member, quoted=True) for member in shape.members
            )
            return [self.alias(wire, f"Union[{members}]")]
        if shape.kind == "record":
            fields = allocate(
                (Symbol(field.id, field.name) for field in shape.fields),
                reserved=RESERVED | frozenset(self.names.values()),
            )
            lines = [f"class {self.reference(wire.id)}(WireValueModel):"]
            if shape.nominal is not None:
                lines.append(
                    f"    __harn_nominal_name__: ClassVar[str | None] = {shape.nominal.name!r}"
                )
            if wire.documentation:
                lines.append(f"    __doc__ = {wire.documentation!r}")
            if shape.additional is not None:
                lines.extend(
                    [
                        '    model_config = ConfigDict(extra="allow")',
                        f"    __pydantic_extra__: dict[str, {self.reference(shape.additional)}] = Field(init=False)",
                    ]
                )
            for field in shape.fields:
                annotation = self.reference(field.type_id)
                default = ""
                if field.optional:
                    annotation += " | MISSING"
                    default = "default=MISSING, "
                lines.append(
                    f"    {fields[field.id]}: {annotation} = Field({default}validation_alias={field.name!r}, serialization_alias={field.name!r})"
                )
            if len(lines) == 1:
                lines.append("    pass")
            return [Declaration("\n".join(lines) + "\n", wire.source)]
        if shape.kind == "enum":
            if not shape.variants:
                raise GenerationError("unsupported_empty_enum", wire)
            # The nominal discriminator is fixed by the Harn declaration, never a Python symbol.
            variants = []
            declarations = []
            for variant in shape.variants:
                name = self.reference(variant_identity(wire.id, variant.id))
                variants.append(repr(name))
                items = (
                    ", ".join(self.reference(field.type_id) for field in variant.fields)
                    or "()"
                )
                content = (
                    f"class {name}(WireValueModel):\n"
                    f"    __harn_wire_kind__: ClassVar[Literal['record', 'enum']] = 'enum'\n"
                    f"    enum_name: Literal[{shape.nominal.name!r}] = Field(validation_alias='enum', serialization_alias='enum')\n"
                    f"    variant: Literal[{variant.name!r}]\n"
                    f"    fields: Annotated[tuple[{items}], BeforeValidator(wire_tuple_validator)]\n"
                )
                declarations.append(Declaration(content, variant.source))
            declarations.append(
                self.alias(
                    wire,
                    variants[0]
                    if len(variants) == 1
                    else "Union[" + ", ".join(variants) + "]",
                    depth=False,
                )
            )
            return declarations
        raise GenerationError("unsupported_wire_type", wire)
