console.log("anh ok");
function chooseFile(fileInput){
    if(fileInput.files && fileInput.files[0]){
        let reader = new FileReader();
        reader.onload = function (e){
            $('.img-profile').attr('src', e.target.result);
        }
        reader.readAsDataURL(fileInput.files[0]);
    }
}