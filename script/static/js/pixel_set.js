const pixel_set_vars = ["k","scale","blur","erode","saturation","contrast",]
function save_pixel_set_to_local_storage(){
    for(let i = 0;i<pixel_set_vars.length;i++)localStorage.setItem(pixel_set_vars[i], document.getElementById(pixel_set_vars[i]).value);
}
function load_pixel_set_to_local_storage(){
    for(let i = 0;i<pixel_set_vars.length;i++)if(localStorage.getItem(pixel_set_vars[i]))document.getElementById(pixel_set_vars[i]).value=localStorage.getItem(pixel_set_vars[i])
}
window.addEventListener('change', save_pixel_set_to_local_storage, false)
window.addEventListener('load', load_pixel_set_to_local_storage, false)