const pixel_set_vars = ["k","scale","blur","erode","saturation","contrast","qr_code_content"]
const pixel_checkbox = ["alpha", "to_tw", "qr_code"]
function save_pixel_set_to_local_storage(){
    for(let i = 0;i<pixel_set_vars.length;i++)localStorage.setItem(pixel_set_vars[i], document.getElementById(pixel_set_vars[i]).value);
    for(let i = 0;i<pixel_checkbox.length;i++)localStorage.setItem(pixel_checkbox[i], document.getElementById(pixel_checkbox[i]).checked);
}
function load_pixel_set_to_local_storage(){
    for(let i = 0;i<pixel_set_vars.length;i++)if(localStorage.getItem(pixel_set_vars[i]))document.getElementById(pixel_set_vars[i]).value=localStorage.getItem(pixel_set_vars[i])
    for(let i = 0;i<pixel_checkbox.length;i++)if(localStorage.getItem(pixel_checkbox[i]))document.getElementById(pixel_checkbox[i]).checked=localStorage.getItem(pixel_checkbox[i])
    qr_code_enable();
}
function qr_code_enable(){
    if(document.getElementById('qr_code').checked==true){
        document.getElementById('qr_code_content').removeAttribute("hidden");
        document.getElementById('qr_code_content_hint').removeAttribute("hidden");
    }
    else{
        document.getElementById('qr_code_content').setAttribute("hidden", "hidden");
        document.getElementById('qr_code_content_hint').setAttribute("hidden", "hidden");
    }
}
window.addEventListener('change', save_pixel_set_to_local_storage, false)
window.addEventListener('load', load_pixel_set_to_local_storage, false)