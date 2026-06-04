# Card de una sala para el catalogo de la pagina de inicio.
# Incluye superposicion de gradiente sobre la imagen, badge de tipo
# con color de acento, y boton de reserva en coral.
import reflex as rx

from studiotrack_frontend.theme import COLORS, FONT_DISPLAY, FONT_BODY, CARD_STYLE
from studiotrack_frontend.state import State


def _badge_tipo(tipo: str) -> rx.Component:
    # El color del badge depende del tipo de sala:
    # grabacion -> morado (acento principal), ensayo -> teal.
    # rx.match evalua el valor reactivo y devuelve el color correspondiente.
    color = rx.match(
        tipo,
        ("grabacion", COLORS["accent_purple"]),
        ("ensayo", COLORS["accent_teal"]),
        COLORS["text_muted"],  # fallback para cualquier otro tipo
    )
    return rx.box(
        rx.text(
            tipo,
            font_family=FONT_BODY,
            font_size="0.7em",
            font_weight="600",
            color="white",
            text_transform="uppercase",
            letter_spacing="0.05em",
        ),
        background=color,
        padding="0.25em 0.7em",
        border_radius="6px",
        # Posicionado sobre la imagen, esquina superior izquierda.
        position="absolute",
        top="0.8em",
        left="0.8em",
        z_index="2",
    )


def sala_card(estudio: dict) -> rx.Component:
    return rx.box(
        # --- Contenedor de imagen con gradiente y badge ---
        rx.box(
            rx.image(
                src=estudio["imagen_url"],
                width="100%",
                height="180px",
                object_fit="cover",
                border_radius="12px",
            ),
            # Superposicion de gradiente: transparente arriba, oscuro abajo.
            # Mejora el contraste del texto que se solapa con la imagen.
            rx.box(
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                border_radius="12px",
                background=(
                    "linear-gradient(to bottom, "
                    "rgba(10,10,15,0) 40%, "
                    "rgba(10,10,15,0.85) 100%)"
                ),
                z_index="1",
            ),
            _badge_tipo(estudio["tipo"]),
            position="relative",
            width="100%",
        ),
        rx.heading(
            estudio["nombre"],
            font_family=FONT_DISPLAY,
            color=COLORS["text_primary"],
            size="5",
            margin_top="0.6em",
        ),
        rx.text(
            estudio["tipo"],
            font_family=FONT_BODY,
            color=COLORS["text_muted"],
            font_size="0.85em",
        ),
        rx.hstack(
            rx.text(
                f"${estudio['precio_hora']}/hora",
                font_family=FONT_BODY,
                color=COLORS["accent_amber"],
                font_weight="600",
            ),
            rx.spacer(),
            rx.text(
                f"Cap. {estudio['capacidad']}",
                font_family=FONT_BODY,
                color=COLORS["text_muted"],
            ),
            width="100%",
            margin_top="0.5em",
        ),
        rx.hstack(
            rx.link(
                rx.button(
                    "Ver detalle",
                    background="transparent",
                    color=COLORS["accent_purple"],
                    border=f"1px solid {COLORS['accent_purple']}",
                    border_radius="8px",
                    cursor="pointer",
                    # color_scheme neutraliza el tema por defecto de Radix.
                    color_scheme="gray",
                    variant="outline",
                ),
                href=f"/sala/{estudio['id']}",
            ),
            rx.button(
                "Reservar",
                on_click=lambda: State.ir_a_reservar(estudio["id"]),
                background=COLORS["accent_coral"],
                color="white",
                border_radius="8px",
                cursor="pointer",
                font_family=FONT_BODY,
                font_weight="600",
                # Forzar coral por encima del tema y en hover.
                _hover={"background": COLORS["accent_coral"], "opacity": "0.85"},
                style={"background_color": f"{COLORS['accent_coral']} !important"},
            ),
            spacing="3",
            margin_top="1em",
        ),
        **CARD_STYLE,
        width="320px",
    )