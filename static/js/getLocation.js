const lat = document.getElementById("lat")
const lon = document.getElementById("lon")

if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
        (position)=>{
            lat.value = position.coords.latitude;
            lon.value = position.coords.longitude;

            console.log(lat, lon);
        },
        (err) => {
            console.log(err.message);
            alert("Erro ao obter localização!");
        }
    );
} else {
    alert("Navegador não suporta geolocalização!");
}
