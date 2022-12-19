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
function init_enable_qrcode(){
    document.getElementById('qr_code').addEventListener('change', qr_code_enable, false);
}
window.addEventListener('load', init_enable_qrcode);