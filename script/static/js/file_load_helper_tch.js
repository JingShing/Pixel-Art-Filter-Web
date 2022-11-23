// script for file name
$('#file_select').click(function(){
    $('#file_input').trigger('click'); 
    }
);

const input = document.getElementById('file_input');
const preview = document.querySelector('.preview');

input.style.opacity = 0;

function init(){
    input.addEventListener('change', updateImageDisplay);
}
window.addEventListener('load', init, false);

function updateImageDisplay() {
    while(preview.firstChild) {
        preview.removeChild(preview.firstChild);
    }

    const curFiles = input.files;
    if (curFiles.length === 0) {
        const para = document.createElement('p');
        para.textContent = '目前沒有選擇檔案';
        preview.appendChild(para);
    } else {
        const list = document.createElement('span');
        preview.appendChild(list);
        for (const file of curFiles) {
        const listItem = document.createElement('span');
        const para = document.createElement('p');
        if (validFileType(file)==1) {
            para.textContent = `檔名： ${file.name}, 尺寸： ${returnFileSize(file.size)}.`;
            const image = document.createElement('img');
            image.src = URL.createObjectURL(file);
            image.width = 200;
            listItem.appendChild(image);
            listItem.appendChild(para);
        }
        else if(validFileType(file)==2){
            para.textContent = `檔名： ${file.name}, 尺寸： ${returnFileSize(file.size)}.`;
            const video = document.createElement('video');
            video.src = URL.createObjectURL(file);
            video.width = 200;
            video.controls = "controls";

            listItem.appendChild(video);
            listItem.appendChild(para);

        }
        else {
            para.textContent = `File name ${file.name}: 並非支持的檔案類型，請重新選取`;
            listItem.appendChild(para);
        }
        list.appendChild(listItem);
        }
    }
}
const fileTypes = [
"image/apng",
"image/bmp",
"image/gif",
"image/jpeg",
"image/pjpeg",
"image/png",
"image/svg+xml",
"image/tiff",
"image/webp",
"image/x-icon",
];
const videoTypes = [
    "video/mp4",
    "video/avi"
]

function validFileType(file) {
    if(fileTypes.includes(file.type))return 1;
    if(videoTypes.includes(file.type))return 2;
    return -1;
}

function returnFileSize(number) {
    if (number < 1024) {
        return `${number} bytes`;
    } else if (number >= 1024 && number < 1048576) {
        return `${(number / 1024).toFixed(1)} KB`;
    } else if (number >= 1048576) {
        return `${(number / 1048576).toFixed(1)} MB`;
    }
}