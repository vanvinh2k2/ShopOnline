
$('#commentForm').submit(function(e){
    e.preventDefault();
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: 'json',
        success: function(res){
            if(res.bool == true){
                let divReview = document.querySelector('.review');
                let titleRes = document.getElementById("title-res");
                titleRes.classList.add("hidden");
                let addviewContent = document.querySelector(".addview-content");
                addviewContent.classList.add("hidden");

                let div = document.createElement("div");
                let html = `
                <div class="review-chat">
                <img src="https://static2.yan.vn/YanNews/2167221/202102/facebook-cap-nhat-avatar-doi-voi-tai-khoan-khong-su-dung-anh-dai-dien-e4abd14d.jpg"/>
                <div class="chat-content">
                    <p>${res.context.user}</p>`;

                for(var i=0; i<res.context.rating; i++){
                    html += `<i class="fas fa-star text-warning"></i>`;
                }

                html += `<p>${res.context.date}</p>
                    <p>${res.context.review}</p>
                </div>
                </div>
                <div class="view"></div>
                <b class="text-success" id="review-res">Review added</b>
                `;
                div.innerHTML = html;
                divReview.appendChild(div);
            }
            
        },
        error: function(res){

        }
    })
});

function progress(arr){
    $.ajax({
        data : arr,
        dataType : "json",
        method : 'get',
        url : "/product-filter/",
        success : function(res){
            let products = document.getElementById("filter-product");
            products.innerHTML = res.data;
        },
        error : function(res){
            console.log("error");
        }
    });
}

let vendorfilter = document.querySelectorAll(".filter-checkbox");
let arrvendor = {};

vendorfilter.forEach((checkbox) => {
    checkbox.addEventListener('click', () => {
        let s = checkbox.getAttribute("data-filter");
        arrvendor[checkbox.getAttribute("data-filter")]=[];
        vendorfilter.forEach((cb_checked)=>{
            if(cb_checked.checked && s === cb_checked.getAttribute("data-filter")){
                arrvendor[cb_checked.getAttribute("data-filter")].push(cb_checked.getAttribute("value"));
            }
        });
        arrvendor['filter-price'] = [];
        arrvendor['filter-price'].push(priceMin.value);
        arrvendor['filter-price'].push(priceMax.value);
        //console.log(arrvendor);
        progress(arrvendor)
    });
  });

  let filterPrice = document.querySelector(".btn-price");
  let priceMin = document.getElementById("minamount");
  let priceMax = document.getElementById("maxamount");
  
function filterPriceFC(){
    filterPrice.addEventListener('click', ()=>{
        arrvendor['filter-price']=[];
        arrvendor['filter-price'].push(priceMin.value);
        arrvendor['filter-price'].push(priceMax.value);
        //console.log(arrvendor);
        progress(arrvendor)
      });
}
  
$(".btn-add-cart").on('click', function(){
    let this_val = $(this).attr("data-index");
    //console.log(this_val+" ok")
    let quantity = $('.product-quantity-'+this_val).val();
    let product_title = $('.product-title-'+this_val).val();
    let product_id = $('.product-id-'+this_val).val();
    let product_pid = $('.product-pid-'+this_val).val();
    let product_image = $('.product-image-'+this_val).val();
    let product_price = $('.product__details__price-'+this_val).attr('value');
    //console.log(quantity+", "+product_title+", "+product_id+", "+product_price+", "+product_pid+", "+product_image);

    $.ajax({
        url : '/add-cart/',
        data : {
            'quantity' : quantity,
            'product_title' : product_title,
            'product_id' : product_id,
            'product_price' : product_price,
            'product_image' : product_image,
            'product_pid' : product_pid
        },
        method : 'get',
        dataType : 'json',
        success : function(res){
            //console.log(res.data);
            alert("Added is success");
            $(".cart-notify").text(res.totalcartitems);
        },
        error : function(res){
            console.log("error!");
        }
    });
});

function delete_cart(x){
        let id_product = x.getAttribute("data-product");
        $.ajax({
            method : 'get',
            url : '/delete-cart/',
            data : {'id': id_product},
            dataType : 'json',
            success : function(res){
                alert("Deleted is success");
                document.querySelector(".cart-notify").innerText = res.totalCartItems+"";
                document.getElementById('cart-list').innerHTML = res.data_cart;
                console.log(res.data_cart);
            },
            error : function(res){
                console.log("error!");
            }
        });
}

function update_cart(x){
            id_product = x.getAttribute("data-product");
            let quantity = $('.product-quantity-'+id_product).val();
            console.log(id_product+" "+quantity);
            $.ajax({
                method : 'get',
                url : '/update-cart/',
                data : {'id': id_product, 'qty' : quantity},
                dataType : 'json',
                success : function(res){
                    alert("Updated is success");
                    document.getElementById('cart-list').innerHTML = res.data_cart;
                    //console.log(res.data_cart);
                },
                error : function(res){
                    console.log("error!");
                }
            });
}

    // Tag
    let tabHeader = document.querySelector(".tab-header");
    let tabContent = document.querySelector(".dashboard-content");

    function tabClick(e){
        let activeEle = tabHeader.querySelector('.active');
        let activeTag = tabContent.querySelector('.active');
        let eleName = e.getAttribute('name');
        let displayTab = tabContent.querySelector('#'+eleName);

        activeEle.classList.remove('active');
        activeTag.classList.remove('active'); 
        e.classList.add('active');
        displayTab.classList.add('active');

    }

$("#add-address").on('click', function(){
    if(checkInputAdd() == true){
        $.ajax({
            url : '/add-address/',
            method : 'get',
            data : {
                'display-name' : $('#display-name').val(),
                'mobile' : $('#phone').val(),
                'address' : $('#address').val()
            },
            dataType : 'json',
            success : function(res){
                $('#exampleModalLong').modal('hide');
                $('.address-main').html(res.data);
            },
            error : function(res){
                console.log("error");
            }
        });
    }
});

function checkInputAdd(){
    if($('#display-name').val() == ""){
        $('#notify-error').text("Error: Please input field Display Name!");
        return false;
    }
    else if($('#phone').val() == ""){
        $('#notify-error').text("Error: Please input field Phone!");
        return false;
    }
    else if($('#address').val() == ""){
        $('#notify-error').text("Error: Please input field Address!");
        return false;
    }
    else {
        $('#notify-error').text("");
        return true;
    };
}

function checkInputUpdate(){
    if($('#display-name-update').val() == ""){
        $('#notify-error-update').text("Error: Please input field Display Name!");
        return false;
    }
    else if($('#phone-update').val() == ""){
        $('#notify-error-update').text("Error: Please input field Phone!");
        return false;
    }
    else if($('#address-update').val() == ""){
        $('#notify-error-update').text("Error: Please input field Address!");
        return false;
    }
    else {
        $('#notify-error-update').text("");
        return true;
    };
}

function add_wishlish(e){
    $.ajax({
        url : '/add-wishlist/',
        data : {'product_id' : e.getAttribute("data-product-item")},
        dataType : 'json',
        method : 'get',
        success : function(res){
            if(res.data == true)
                alert("Added into Wishlist.");
            else alert("Add fail.");
        },
        error : function(){
            console.log("Error!");
        }
    });
}

function address_default(e){
    $.ajax({
        url : '/address-default/',
        data : {'address_id' : e.getAttribute('data-address')},
        dataType : 'json',
        method : 'get',
        success : function(res){
            $('.address-main').html(res.data);
        },
        error : function(){
            console.log("Error.");
        }
    });
}

function update_address(){
    if(checkInputUpdate() == true){
        $.ajax({
            url : '/update-address/',
            method : 'get',
            data : {
                'address_id' : $("#update-address").attr("data-address-id"),
                'display-name' : $('#display-name-update').val(),
                'mobile' : $('#phone-update').val(),
                'address' : $('#address-update').val()
            },
            dataType : 'json',
            success : function(res){
                $('#exampleModalLong2').modal('hide');
                $('.address-main').html(res.data);
            },
            error : function(res){
                console.log("error");
            }
        });
    }
}

function displayDataUpdate(e){
    $.ajax({
        url : '/display-data-update/',
        method : 'get',
        data : {
            'address_id' : e.getAttribute('data-update')
        },
        dataType : 'json',
        success : function(res){
            $('#modal-content-update').html(res.data);
        },
        error : function(res){
            console.log("error");
        }
    });
}

function save_profile(){
    //console.log('image/'+$('#img-choice')[0].files[0].name);
    $.ajax({
        url : '/save-profile/',
        data : {
            'full_name' : $('#full-name').val(),
            'bio' : $('#bio').val(),
            'email' : $('#email').val(),
            'phone' : $('#phone').val(),
            'image' : 'image/'+$('#img-choice')[0].files[0].name
        },
        dataType : 'json',
        method : 'get',
        success : function(res){
            $('#profile-content').html(res.data);
            alert("Save successful.")
        },
        error : function(){
            console.log("Error!");
        }
    });
}

function deleteWishList(e){
    let wishlist_id = e.getAttribute("data-product");
    $.ajax({
        url : '/delete-wishlist',
        data : {
            'wishlist-id' : wishlist_id
        },
        dataType : 'json',
        method : 'get',
        success : function(res){
            console.log("TCR");
            $('.content-wishlist').html(res.data);
            alert("Delete success.");
        },
        error : function(res){
            console.log("Error!");
        }
    });
}