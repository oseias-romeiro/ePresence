const lat = document.getElementById("lat")
const lon = document.getElementById("lon")

if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
        (position)=>{
            lat.value = position.coords.latitude;
            lon.value = position.coords.longitude;

            console.log(lat.value, lon.value);
            alert("Location getted :D");
        },
        (err) => {
            console.log(err.message);
            alert("Error get location!");
        }
    );
} else {
    alert("Browser not support location!");
}
