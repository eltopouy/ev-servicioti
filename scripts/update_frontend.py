# -*- coding: utf-8 -*-
"""
Script para actualizar renderCatalogWithList y openVehicleModal en index.html
con logos prominentes, año de origen y arquitectura completa de baterías.
"""

def main():
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Reemplazo de renderCatalogWithList
    start_str = "    function renderCatalogWithList(list) {"
    end_str = "    const VISTA_LABELS = ["
    
    start_idx = html.find(start_str)
    end_idx = html.find(end_str)
    assert start_idx != -1, "start_str not found"
    assert end_idx != -1, "end_str not found"

    new_render_catalog = """    function renderCatalogWithList(list) {
      const grid = document.getElementById('catalog-grid');
      if (!list || list.length === 0) {
        grid.innerHTML = `
          <div class="col-span-1 md:col-span-2 lg:col-span-3 py-12 text-center text-muted space-y-3">
            <span class="text-4xl block">🔍</span>
            <p class="text-sm font-editorial text-neutral-800 font-bold">No se encontraron vehículos que coincidan con los filtros aplicados.</p>
            <button onclick="filterByBrand('todas'); filterCatalog('todos');" class="text-xs bg-neutral-900 text-white px-3 py-1.5 rounded font-semibold hover:bg-neutral-800 transition">
              Restablecer todos los filtros
            </button>
          </div>
        `;
        return;
      }

      grid.innerHTML = list.map(v => {
        const isPixel = (currentViewMode === 'pixel');
        const imgSrc = isPixel 
          ? (v.especificaciones?.pixel_art_url || v.imagen_oficial_url)
          : v.imagen_oficial_url;
        const badgeSrc = v.especificaciones?.badge_circular_url || v.imagen_oficial_url;
        const imgClass = isPixel 
          ? 'w-full h-full object-contain image-pixelated p-4 group-hover:scale-110 transition duration-300' 
          : 'w-full h-full object-cover group-hover:scale-105 transition duration-300';

        const batTipoSimple = v.bateria_tipo ? v.bateria_tipo.split('(')[0].trim() : 'Litio';

        return `
        <div onclick="openVehicleModal('${v.id}')" class="bg-white rounded-lg border ${v.es_top_ventas ? 'border-amber-300 shadow-amber-100' : 'border-line'} p-4 space-y-3 hover:border-neutral-900 transition flex flex-col justify-between cursor-pointer group shadow-sm hover:shadow-md">
          <div class="space-y-3">
            <div class="aspect-[4/5] sm:aspect-[4/3] w-full bg-neutral-100 rounded overflow-hidden relative">
              <img src="${imgSrc}" alt="${v.marca} ${v.modelo} ${v.version || ''} - Vehículo Eléctrico en Uruguay - EV ServicioTI" loading="lazy" class="${imgClass}">
              <span class="absolute top-2 left-2 bg-white/95 px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider text-neutral-900 rounded border border-line">
                ${v.tipo}
              </span>
              <span class="absolute bottom-2 right-2 bg-neutral-900/90 text-white text-[10px] font-medium px-2 py-0.5 rounded backdrop-blur">
                📸 ${v.galeria ? v.galeria.length : 6} fotos
              </span>
            </div>

            ${v.es_top_ventas ? `
              <div class="bg-gradient-to-r from-amber-400 to-amber-300 text-neutral-950 px-2.5 py-1 rounded text-[10px] font-bold tracking-wide flex items-center justify-between shadow-sm">
                <span>🏆 #${v.ventas_rank} MÁS VENDIDO EN URUGUAY</span>
                <span class="font-normal opacity-90">${v.unidades_anuales ? v.unidades_anuales.toLocaleString() + ' empadronados' : 'Oficial ACAU'}</span>
              </div>
            ` : ''}

            <div class="flex items-start gap-3">
              <div class="relative shrink-0 mt-0.5">
                <img src="${badgeSrc}" alt="Badge ${v.marca} ${v.modelo}" class="w-10 h-10 rounded-full border border-neutral-300 object-cover shadow-xs">
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex items-center justify-between gap-1 mb-1">
                  <div class="flex items-center gap-1.5 min-w-0 flex-wrap">
                    ${v.brand_logo_url ? `<img src="${v.brand_logo_url}" alt="Logo ${v.marca}" class="h-5 max-w-[70px] object-contain bg-white px-1 py-0.5 rounded border border-neutral-200 shrink-0 shadow-2xs">` : ''}
                    <span class="text-xs uppercase font-mono tracking-wider font-bold text-neutral-800 truncate">${v.marca}</span>
                    ${v.anio_origen ? `<span class="text-[9px] font-mono text-neutral-500 bg-neutral-100 px-1.5 py-0.2 rounded border border-neutral-200 shrink-0">Año ${v.anio_origen}</span>` : ''}
                  </div>
                  ${v.brand_instagram_handle ? `
                    <a href="${v.brand_instagram_url}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" class="text-[10px] font-mono font-medium text-pink-700 bg-pink-50 hover:bg-pink-100 border border-pink-200 px-1.5 py-0.5 rounded flex items-center gap-1 transition shrink-0" title="Ver Instagram Oficial en Uruguay">
                      <svg class="w-2.5 h-2.5 fill-current" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                    </a>
                  ` : ''}
                </div>
                <h3 class="text-xl font-bold font-editorial text-neutral-950 group-hover:text-accent transition truncate">${v.modelo} <span class="text-sm font-normal text-muted">${v.version || ''}</span></h3>
                <div class="text-lg font-extrabold text-neutral-900 font-editorial mt-0.5">USD $${v.precio_usd.toLocaleString()}</div>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2 text-xs py-2 border-y border-line text-neutral-700">
              <div>
                <span class="text-muted block text-[10px]">Autonomía:</span> 
                <b>${v.autonomia_km} km</b>
              </div>
              <div>
                <span class="text-muted block text-[10px]">Batería:</span> 
                <b>${v.bateria_kwh} kWh</b>
                <span class="text-[10px] text-emerald-800 font-mono block truncate font-medium">${batTipoSimple}</span>
              </div>
            </div>

            <div class="text-xs text-neutral-600 space-y-1">
              <div><span class="font-medium text-neutral-800">Conector:</span> ${v.conector}</div>
              <div><span class="font-medium text-neutral-800">Garantía:</span> ${v.garantia_bateria}</div>
            </div>
          </div>

          <div class="pt-3 border-t border-line flex items-center justify-between text-xs">
            <span class="text-emerald-700 font-semibold text-[11px]">✓ Homologado URSEA</span>
            <span class="font-semibold text-neutral-900 group-hover:text-accent flex items-center gap-1">
              Ver 6 Vistas & Ficha →
            </span>
          </div>
        </div>
      `;
      }).join('');
    }

"""

    html = html[:start_idx] + new_render_catalog + html[end_idx:]

    # 2. Reemplazo de openVehicleModal
    start_modal = "    function openVehicleModal(vehicleId) {"
    end_modal = "    function changeModalImage(imgUrl, btn, viewTitle, currIdx, total, isPixel = false) {"
    
    start_m_idx = html.find(start_modal)
    end_m_idx = html.find(end_modal)
    assert start_m_idx != -1, "start_modal not found"
    assert end_m_idx != -1, "end_modal not found"

    new_modal_code = """    function openVehicleModal(vehicleId) {
      const v = (appData.vehicles || []).find(item => item.id === vehicleId);
      if (!v) return;

      document.getElementById('modal-brand').textContent = v.marca;
      document.getElementById('modal-title').textContent = `${v.marca} ${v.modelo}`;
      document.getElementById('modal-version').textContent = v.version || '';
      document.getElementById('modal-price').textContent = `USD $${v.precio_usd.toLocaleString()}`;

      // Configurar Badge Circular Oficial y Logo de Marca en el Header del Modal
      const badgeImg = document.getElementById('modal-circular-badge');
      if (badgeImg) {
        badgeImg.src = v.especificaciones?.badge_circular_url || v.imagen_oficial_url;
      }
      const brandLogoImg = document.getElementById('modal-brand-logo');
      if (brandLogoImg) {
        if (v.brand_logo_url) {
          brandLogoImg.src = v.brand_logo_url;
          brandLogoImg.classList.remove('hidden');
        } else {
          brandLogoImg.classList.add('hidden');
        }
      }

      // Año de origen en el header
      const yearChip = document.getElementById('modal-year-origin-chip');
      if (yearChip) {
        yearChip.textContent = v.anio_origen ? `Año ${v.anio_origen}` : '';
      }

      // Instagram Oficial en el Header
      const instaHeader = document.getElementById('modal-brand-instagram-container');
      if (instaHeader) {
        if (v.brand_instagram_handle) {
          instaHeader.innerHTML = `
            <a href="${v.brand_instagram_url}" target="_blank" rel="noopener noreferrer" class="text-[10px] font-mono font-medium text-pink-700 bg-pink-50 hover:bg-pink-100 border border-pink-200 px-1.5 py-0.5 rounded flex items-center gap-1 transition">
              <svg class="w-2.5 h-2.5 fill-current" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
              ${v.brand_instagram_handle}
            </a>
          `;
        } else {
          instaHeader.innerHTML = '';
        }
      }

      // Box de Representación Oficial
      const impName = document.getElementById('modal-importer-name');
      if (impName) {
        impName.textContent = v.brand_importador || 'Distribución y garantía oficial homologada en Uruguay';
      }
      const brandActions = document.getElementById('modal-brand-actions');
      if (brandActions) {
        let actHtml = '';
        if (v.brand_instagram_handle) {
          actHtml += `
            <a href="${v.brand_instagram_url}" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold text-pink-700 bg-pink-50 hover:bg-pink-100 border border-pink-200 px-2 py-0.5 rounded flex items-center gap-1 transition">
              Instagram Oficial ↗
            </a>
          `;
        }
        if (v.brand_sitio_oficial) {
          actHtml += `
            <a href="${v.brand_sitio_oficial}" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold text-neutral-700 bg-white hover:bg-neutral-100 border border-neutral-300 px-2 py-0.5 rounded flex items-center gap-1 transition">
              Web Marca ↗
            </a>
          `;
        }
        brandActions.innerHTML = actHtml;
      }

      // Badge de Líder en Ventas en el Modal
      const topBadge = document.getElementById('modal-top-sales-badge');
      if (v.es_top_ventas) {
        topBadge.innerHTML = `
          <div class="bg-amber-50 border border-amber-300 rounded-lg p-3 text-xs text-amber-950 font-medium flex items-center justify-between shadow-sm">
            <div class="flex items-center gap-2.5">
              <span class="text-xl">🏆</span>
              <div>
                <span class="font-bold text-amber-900 block text-sm">Líder de Ventas Oficial en Uruguay — Puesto #${v.ventas_rank}</span>
                <span class="text-[11px] text-amber-800">
                  Ranking oficial de empadronamientos ACAU / SUCIVE con <b>${v.unidades_anuales ? v.unidades_anuales.toLocaleString() : ''} unidades registradas</b> en plaza.
                </span>
              </div>
            </div>
            <span class="bg-amber-400 text-neutral-950 text-[10px] font-black uppercase px-2 py-1 rounded tracking-wide">
              TOP VENTAS
            </span>
          </div>
        `;
        topBadge.classList.remove('hidden');
      } else {
        topBadge.classList.add('hidden');
      }

      // Configurar imagen principal y miniaturas de galería de 6 vistas + Pixel Art
      const galeria = v.galeria && v.galeria.length > 0 ? v.galeria : [v.imagen_oficial_url];
      const mainImg = document.getElementById('modal-main-img');
      mainImg.src = galeria[0];
      mainImg.alt = `${v.marca} ${v.modelo} ${v.version || ''} - Galería Oficial - EV Uruguay`;
      mainImg.classList.remove('image-pixelated');

      // Título y Contador inicial
      document.getElementById('modal-view-title').textContent = VISTA_LABELS[0];
      document.getElementById('modal-view-counter').textContent = `Foto 1 de ${galeria.length}`;

      const thumbsContainer = document.getElementById('modal-thumbs');
      let thumbsHtml = galeria.map((imgUrl, idx) => {
        const lbl = VISTA_LABELS[idx] || `Vista 0${idx + 1}`;
        return `
          <button onclick="changeModalImage('${imgUrl}', this, '${lbl}', ${idx + 1}, ${galeria.length}, false)" aria-label="Ver foto ${idx + 1}" class="modal-thumb w-20 h-16 rounded overflow-hidden border-2 border-transparent opacity-75 hover:opacity-100 transition shrink-0 relative ${idx === 0 ? 'thumb-active' : ''}">
            <img src="${imgUrl}" alt="${v.marca} ${v.modelo} - ${lbl} - EV Uruguay" loading="lazy" class="w-full h-full object-cover">
            <span class="absolute bottom-0.5 right-0.5 bg-neutral-900/85 text-white text-[9px] font-mono px-1 rounded font-bold">${idx + 1}</span>
          </button>
        `;
      }).join('');

      if (v.especificaciones?.pixel_art_url) {
        thumbsHtml += `
          <button onclick="changeModalImage('${v.especificaciones.pixel_art_url}', this, '👾 Icono Coleccionable Pixel Art 16-Bit', 'Pixel', 'Retro', true)" aria-label="Ver Pixel Art" class="modal-thumb w-20 h-16 rounded overflow-hidden border-2 border-transparent bg-neutral-900 p-1 opacity-75 hover:opacity-100 transition shrink-0 relative flex flex-col items-center justify-center text-center">
            <img src="${v.especificaciones.pixel_art_url}" alt="Pixel Art ${v.marca} ${v.modelo}" class="w-10 h-10 object-contain image-pixelated">
            <span class="text-[8px] font-mono font-bold text-amber-300">16-BIT</span>
          </button>
        `;
      }

      thumbsContainer.innerHTML = thumbsHtml;

      // Ficha técnica
      document.getElementById('spec-range').textContent = `${v.autonomia_km} km`;
      document.getElementById('spec-battery').textContent = `${v.bateria_kwh} kWh`;
      document.getElementById('spec-power').textContent = v.potencia || '-';
      document.getElementById('spec-torque').textContent = v.par_motor_nm ? `${v.par_motor_nm} Nm` : '-';
      document.getElementById('spec-accel').textContent = v.aceleracion_0_100 || '-';
      document.getElementById('spec-topspeed').textContent = v.velocidad_maxima || '-';

      document.getElementById('spec-connector').textContent = v.conector || '-';
      document.getElementById('spec-ac').textContent = v.tiempo_carga_ac || '-';
      document.getElementById('spec-dc').textContent = v.tiempo_carga_dc || '-';
      document.getElementById('spec-dims').textContent = v.dimensiones || '-';
      document.getElementById('spec-trunk').textContent = v.capacidad_baul_l ? `${v.capacidad_baul_l} L` : '-';
      document.getElementById('spec-warranty-car').textContent = v.garantia_vehiculo || '-';
      document.getElementById('spec-warranty-battery').textContent = v.garantia_bateria || '-';

      // Arquitectura de Batería & Propulsión de Alto Voltaje en el Modal
      const elBatTipo = document.getElementById('spec-bat-tipo');
      if (elBatTipo) elBatTipo.textContent = v.bateria_tipo || 'Batería de Iones de Litio';

      const elBatQuimica = document.getElementById('spec-bat-quimica');
      if (elBatQuimica) elBatQuimica.textContent = v.bateria_quimica || 'Química estándar de litio de alta densidad';

      const elBatFab = document.getElementById('spec-bat-fabricante');
      if (elBatFab) elBatFab.textContent = v.bateria_fabricante || 'Fabricante Homologado';

      const elBatRefrig = document.getElementById('spec-bat-refrig');
      if (elBatRefrig) elBatRefrig.textContent = v.bateria_refrigeracion || 'Gestión térmica inteligente';

      const elBatVolt = document.getElementById('spec-bat-voltaje');
      if (elBatVolt) elBatVolt.textContent = v.bateria_voltaje || 'Arquitectura de alto voltaje';

      const elBatAnio = document.getElementById('spec-bat-anio');
      if (elBatAnio) elBatAnio.textContent = v.anio_origen ? `${v.anio_origen} (Lanzamiento en origen)` : 'En plaza comercial';

      const elBatBadge = document.getElementById('modal-battery-badge');
      if (elBatBadge) {
        elBatBadge.textContent = v.bateria_quimica ? v.bateria_quimica.split(' ')[0] : '100% Eléctrico';
      }

      // Enlace oficial
      const officialBtn = document.getElementById('modal-official-link');
      officialBtn.href = v.link_fabricante;

      // Especificaciones extra
      const extraDiv = document.getElementById('modal-extra-specs');
      const specs = v.especificaciones || {};
      const keys = Object.keys(specs).filter(k => k !== 'badge_circular_url' && k !== 'pixel_art_url');
      if (keys.length > 0) {
        extraDiv.innerHTML = keys.map(k => `
          <div><b class="capitalize text-neutral-900">${k.replace(/_/g, ' ')}:</b> ${specs[k]}</div>
        `).join('');
        extraDiv.classList.remove('hidden');
      } else {
        extraDiv.classList.add('hidden');
      }

      // Datos de TCO, Patente SUCIVE, Seguro BSE y Service Oficial en el Modal
      const patenteVal = v.patente_anual_estimada_uyu || 0;
      const seguroVal = v.seguro_anual_estimado_uyu || 0;
      const serviceUsd = v.service_costo_usd || 140;
      const serviceKm = v.service_intervalo_km || 20000;
      const taller = v.service_taller_oficial || 'Taller Oficial del Importador';

      const elPat = document.getElementById('modal-patente-val');
      if (elPat) elPat.textContent = (patenteVal > 0) ? `$${Math.round(patenteVal).toLocaleString()} UYU / año` : 'Exento (0 UYU)';
      
      const elSeg = document.getElementById('modal-seguro-val');
      if (elSeg) elSeg.textContent = `$${Math.round(seguroVal).toLocaleString()} UYU / año`;

      const elServ = document.getElementById('modal-service-val');
      if (elServ) elServ.textContent = `USD $${serviceUsd} (~$${Math.round(serviceUsd * 41).toLocaleString()} UYU)`;

      const elServFreq = document.getElementById('modal-service-freq');
      if (elServFreq) elServFreq.textContent = `Cada ${serviceKm.toLocaleString()} km o 1 año`;

      const elTaller = document.getElementById('modal-taller-val');
      if (elTaller) elTaller.textContent = taller;

      let tareasText = 'Diagnóstico computarizado de batería de alto voltaje, filtro de habitáculo, líquido de frenos y actualización de software.';
      if (v.mantenimiento_detalle_json) {
        try {
          const mDet = (typeof v.mantenimiento_detalle_json === 'string') 
            ? JSON.parse(v.mantenimiento_detalle_json) 
            : v.mantenimiento_detalle_json;
          tareasText = mDet.tareas_incluidas || tareasText;
        } catch(e) {}
      }
      const elTasks = document.getElementById('modal-service-tasks');
      if (elTasks) elTasks.textContent = tareasText;

      document.getElementById('vehicle-modal').classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }

"""

    html = html[:start_m_idx] + new_modal_code + html[end_m_idx:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html actualizado exitosamente!")

if __name__ == "__main__":
    main()
