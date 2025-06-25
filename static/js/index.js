// Variables globales para las capas
var map;
var incidentLayer;
var zonasSegurasLayer;
var zonasPeligrosasLayer;
var layerGroup;
var markersCluster;

// Función para inicializar el mapa
function initMap() {
    map = L.map('map').setView([-12.0600, -77.0300], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    layerGroup = L.featureGroup();
    markersCluster = L.markerClusterGroup();
}

// Función para cargar todos los datos
function loadAllData() {
    document.getElementById('loading-message').style.display = 'block';

    // Cargar todos los endpoints en paralelo
    Promise.all([
        fetchData('/incidentes'),
        fetchData('/zonas_seguridad'),
        fetchData('/zonas_peligrosas')
    ])
        .then(([incidentes, zonasSeguras, zonasPeligrosas]) => {
            processIncidentes(incidentes);
            processZonasSeguras(zonasSeguras);
            processZonasPeligrosas(zonasPeligrosas);

            // Ajustar vista después de cargar todo
            if (layerGroup.getLayers().length > 0) {
                map.fitBounds(layerGroup.getBounds(), { padding: [20, 20] });
            }

            document.getElementById('loading-message').style.display = 'none';
        })
        .catch(error => {
            console.error('Error al cargar datos:', error);
            document.getElementById('loading-message').style.display = 'none';
            alert('Error al cargar algunos datos. Por favor revise la consola para más detalles.');
        });
}

// Función genérica para fetch
function fetchData(endpoint) {
    return fetch(`http://localhost:5000${endpoint}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en ${endpoint}: ${response.status}`);
            }
            return response.json();
        });
}

// Procesar incidentes con clusterización
function processIncidentes(data) {
    if (!data.features || data.features.length === 0) {
        console.log('No hay datos de incidentes');
        return;
    }

    incidentLayer = L.geoJSON(data, {
        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, {
                radius: 8,
                fillColor: "#ff0000",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            });
        },
        onEachFeature: function (feature, layer) {
            var popupText = `<b>Tipo:</b> ${feature.properties.tipo}<br>
                          <b>Fecha:</b> ${new Date(feature.properties.fecha).toLocaleDateString()}<br>
                          <b>Descripción:</b> ${feature.properties.descripcion}<br>
                          <b>Advertencia:</b> Área peligrosa`;
            layer.bindPopup(popupText);
        }
    });

    markersCluster.addLayer(incidentLayer);
    layerGroup.addLayer(markersCluster);
    map.addLayer(markersCluster);

    // Configurar evento del checkbox
    document.getElementById('incidentes-checkbox').addEventListener('change', function (e) {
        if (e.target.checked) {
            map.addLayer(markersCluster);
        } else {
            map.removeLayer(markersCluster);
        }
    });
}

// Procesar zonas seguras
function processZonasSeguras(data) {
    if (!data.features || data.features.length === 0) {
        console.log('No hay datos de zonas seguras');
        return;
    }

    zonasSegurasLayer = L.geoJSON(data, {
        style: function () {
            return {
                color: "#00FF00",
                weight: 2,
                opacity: 0.8,
                fillOpacity: 0.3
            };
        },
        onEachFeature: function (feature, layer) {
            var popupText = `<b>Nombre:</b> ${feature.properties.nombre}<br>
                          <b>Descripción:</b> ${feature.properties.descripcion}<br>
                          <b>Estatus:</b> Zona segura`;
            layer.bindPopup(popupText);
        }
    });

    layerGroup.addLayer(zonasSegurasLayer);
    map.addLayer(zonasSegurasLayer);

    // Configurar evento del checkbox
    document.getElementById('seguras-checkbox').addEventListener('change', function (e) {
        if (e.target.checked) {
            map.addLayer(zonasSegurasLayer);
        } else {
            map.removeLayer(zonasSegurasLayer);
        }
    });
}

// Procesar zonas peligrosas
function processZonasPeligrosas(data) {
    if (!data.features || data.features.length === 0) {
        console.log('No hay datos de zonas peligrosas');
        return;
    }

    zonasPeligrosasLayer = L.geoJSON(data, {
        style: function () {
            return {
                color: "#FF0000",
                weight: 2,
                opacity: 0.8,
                fillOpacity: 0.3
            };
        },
        onEachFeature: function (feature, layer) {
            var popupText = `<b>Nombre:</b> ${feature.properties.nombre}<br>
                          <b>Descripción:</b> ${feature.properties.descripcion}<br>
                          <b>Advertencia:</b> Zona muy peligrosa`;
            layer.bindPopup(popupText);
        }
    });

    layerGroup.addLayer(zonasPeligrosasLayer);
    map.addLayer(zonasPeligrosasLayer);

    // Configurar evento del checkbox
    document.getElementById('peligrosas-checkbox').addEventListener('change', function (e) {
        if (e.target.checked) {
            map.addLayer(zonasPeligrosasLayer);
        } else {
            map.removeLayer(zonasPeligrosasLayer);
        }
    });
}

// Configurar filtro por fecha
document.getElementById('fecha-filter').addEventListener('change', function (e) {
    var selectedDate = e.target.value;
    if (selectedDate) {
        // Aquí implementarías la lógica para filtrar por fecha
        console.log('Filtrar por fecha:', selectedDate);
        alert('Filtrado por fecha sería implementado aquí. Se necesita modificar el backend para soportar este filtro.');
    } else {
        // Mostrar todos los datos si no hay fecha seleccionada
        console.log('Mostrar todos los datos');
    }
});

// Inicializar el mapa y cargar datos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
    initMap();
    loadAllData();
});