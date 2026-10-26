# -*- coding: utf-8 -*-
"""
Servicio de Inyección de Metadatos y Optimización de Imágenes para EV Uruguay (ev.servicioti.com.uy).
Reutiliza el estándar de blindaje de metadatos (XMP UTF-8 + EXIF Unicode) de ServicioTI.
Purga cualquier rastro de rutas locales y optimiza el archivo a WebP / JPEG progresivo de peso mínimo.
"""

import os
import io
import re
import html
from pathlib import Path
from typing import Optional, List
from PIL import Image, ExifTags

AUTOR_OFICIAL = "Andrés Franchi Ugartemendía"
AUTOR_ASCII = "Andres Franchi Ugartemendia"
URL_OFICIAL = "https://ev.servicioti.com.uy"
URL_SERVICIO_TI = "https://servicioti.com.uy"
COPYRIGHT_TEXTO = f"Copyright © 2026 {AUTOR_OFICIAL}. Todos los derechos reservados. - {URL_OFICIAL}"
COPYRIGHT_ASCII = f"Copyright (c) 2026 {AUTOR_ASCII} - {URL_OFICIAL}"
CREDITO_OFICIAL = f"{AUTOR_OFICIAL} - ServicioTI (EV Uruguay)"
SOFTWARE_TAG = "ServicioTI EV Visual Engine (ev.servicioti.com.uy)"

class MetadataImageService:
    """Gestiona la inyección de metadatos y compresión ultraligera sin pérdida perceptible."""

    @classmethod
    def _construir_paquete_xmp(
        cls,
        titulo: str,
        descripcion: str,
        categoria: str = "Movilidad Eléctrica",
        keywords: Optional[List[str]] = None
    ) -> str:
        """Construye el XML/RDF de XMP en UTF-8 nativo para Google Images y Discover."""
        t_esc = html.escape(titulo or "Vehículo Eléctrico en Uruguay")
        d_esc = html.escape(descripcion or "Directorio y análisis de vehículos eléctricos en Uruguay - ServicioTI.")
        c_esc = html.escape(categoria.capitalize() if categoria else "Movilidad Eléctrica")

        lista_kw = keywords or [
            "EV Uruguay", "Autos Eléctricos Uruguay", "Movilidad Sostenible",
            "Montevideo", "ServicioTI", AUTOR_OFICIAL, c_esc
        ]
        items_kw = "".join(f"<rdf:li>{html.escape(k)}</rdf:li>" for k in lista_kw)

        xmp_xml = f"""<?xpacket begin='' id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x='adobe:ns:meta/'>
 <rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about=''
    xmlns:dc='http://purl.org/dc/elements/1.1/'
    xmlns:xmp='http://ns.adobe.com/xap/1.0/'
    xmlns:xmpRights='http://ns.adobe.com/xap/1.0/rights/'
    xmlns:photoshop='http://ns.adobe.com/photoshop/1.0/'>
   <dc:creator>
    <rdf:Seq><rdf:li>{AUTOR_OFICIAL}</rdf:li></rdf:Seq>
   </dc:creator>
   <dc:title>
    <rdf:Alt><rdf:li xml:lang='x-default'>{t_esc}</rdf:li></rdf:Alt>
   </dc:title>
   <dc:description>
    <rdf:Alt><rdf:li xml:lang='x-default'>{d_esc}</rdf:li></rdf:Alt>
   </dc:description>
   <dc:rights>
    <rdf:Alt><rdf:li xml:lang='x-default'>{COPYRIGHT_TEXTO}</rdf:li></rdf:Alt>
   </dc:rights>
   <dc:subject>
    <rdf:Bag>{items_kw}</rdf:Bag>
   </dc:subject>
   <xmpRights:Marked>True</xmpRights:Marked>
   <xmpRights:WebStatement>{URL_OFICIAL}</xmpRights:WebStatement>
   <photoshop:Credit>{CREDITO_OFICIAL}</photoshop:Credit>
   <photoshop:Source>{URL_OFICIAL}</photoshop:Source>
   <photoshop:Category>{c_esc}</photoshop:Category>
   <xmp:CreatorTool>{SOFTWARE_TAG}</xmp:CreatorTool>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end='w'?>"""
        return xmp_xml

    @classmethod
    def inyectar_y_optimizar(
        cls,
        ruta_imagen: Path,
        titulo: str,
        descripcion: str = "",
        calidad: int = 80,
        destino: Optional[Path] = None,
        formato: str = "WEBP"
    ) -> bool:
        """
        Inyecta metadatos oficiales de ServicioTI y comprime la imagen al menor peso posible.
        Si se especifica destino, guarda el resultado directamente en esa ruta en formato WEBP.
        """
        path_origen = Path(ruta_imagen)
        if not path_origen.exists():
            return False

        path_destino = Path(destino) if destino else path_origen

        try:
            with Image.open(path_origen) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # 1. Preparar bloque EXIF limpio
                exif = Image.Exif()
                comentario_unicode = f"EV Uruguay • {URL_OFICIAL} • {AUTOR_OFICIAL} • {titulo[:100]}"
                exif[ExifTags.Base.UserComment] = b"UNICODE\x00" + comentario_unicode.encode("utf-16le")
                exif[ExifTags.Base.Artist] = AUTOR_ASCII
                exif[ExifTags.Base.Copyright] = COPYRIGHT_ASCII
                exif[ExifTags.Base.Software] = SOFTWARE_TAG
                desc_limpia = re.sub(r"[^\x20-\x7EáéíóúÁÉÍÓÚñÑüÜ¿¡.,;:\-]", " ", descripcion or titulo)[:180]
                exif[ExifTags.Base.ImageDescription] = desc_limpia.encode("latin-1", errors="replace").decode("latin-1")

                # 2. XMP UTF-8
                xmp_xml = cls._construir_paquete_xmp(titulo=titulo, descripcion=descripcion)

                buf = io.BytesIO()
                fmt = formato.upper() if formato else ("WEBP" if path_destino.suffix.lower() == ".webp" else "JPEG")

                if fmt == "WEBP" or path_destino.suffix.lower() == ".webp":
                    img.save(
                        buf,
                        format="WEBP",
                        quality=calidad,
                        method=6,
                        exif=exif,
                        xmp=xmp_xml.encode("utf-8")
                    )
                else:
                    img.save(
                        buf,
                        format="JPEG",
                        quality=calidad,
                        optimize=True,
                        progressive=True,
                        subsampling=1,
                        exif=exif,
                        xmp=xmp_xml.encode("utf-8")
                    )

                datos_finales = buf.getvalue()

            path_destino.parent.mkdir(parents=True, exist_ok=True)
            with open(path_destino, "wb") as f_out:
                f_out.write(datos_finales)

            print(f"[Metadatos] Imagen optimizada con autoría ServicioTI: {path_destino.name} ({len(datos_finales)/1024:.1f} KB)")
            return True

        except Exception as e:
            print(f"[Metadatos] Error al procesar {path_destino.name}: {e}")
            return False
            return True

        except Exception as e:
            print(f"[Metadatos] Error al procesar {path.name}: {e}")
            return False
