
document.getElementById("btn-download").addEventListener("click", function() {
    var element = document.getElementById("content");
    var opt = {
        margin: 1,
        filename: 'shop_online.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
      };
    html2pdf().from(element).set(opt).save();
  });