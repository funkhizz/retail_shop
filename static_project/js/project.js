$(document).ready(function(){
    // Contact form Handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")

    function displaySubmit(submitBtn, defaultText, doSubmit){

        if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
        } else {
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)
        }

    }

    contactForm.submit(function(event) {
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmit(contactFormSubmitBtn, "", true)
        $.ajax({
        method: contactFormMethod,
        url: contactFormEndpoint,
        data: contactFormData,
        success: function(data) {
            thisForm[0].reset()
            $.alert({
            title: "Success!",
            content: data.message,
            theme: "modern",
        })
        setTimeout(function(){
            displaySubmit(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 500)
        },
        error: function(error){
            console.log(error.responseJSON)
            var jsonData = error.responseJSON
            var msg = ""
            $.each(jsonData, function(key, value){
            msg += key + ": " + value[0].message
            })

            $.alert({
            title: "Wait!",
            content: msg,
            theme: "modern",
        })
        setTimeout(function(){
            displaySubmit(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 500)
        },
        })
    })
    // Auto search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']") // input name='q'
    var typingTimer;
    var typingInterval = 500 // 0.5 seconds
    var searchBtn = searchForm.find("[type='submit']")


    searchInput.keyup(function(event){
        // key released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })

    searchInput.keydown(function(event){
        // key pressed
        clearTimeout(typingTimer)
    })

    function displaySearching(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
    }

    function performSearch(){
        displaySearching()
        var query = searchInput.val()
        setTimeout(function(){
        window.location.href = "/search/?q=" + query
        }, 1000)
        }

    // Cart + Add/Remove products
    var productForm = $(".form-product-ajax")
    productForm.submit(function(event) {
    event.preventDefault();
    var thisForm = $(this)
    // var actionEndpoint = thisForm.attr('action');
    var actionEndpoint = thisForm.attr('data-endpoint');
    var httpMethod = thisForm.attr('method');
    var formData = thisForm.serialize();
    $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
        var submitSpan = thisForm.find(".submit-span")
            if (data.added){
            submitSpan.html('<button class="btn btn-info" type="submit">Remove</button>')
            } else {
            submitSpan.html('<button class="btn btn-success" type="submit">Add to cart</button>')
            }
            var navbarCount = $(".navbar-cart-count")

            if (data.count != 0) {
            navbarCount.text(" " + data.count)
            } else {
            navbarCount.text("")
            }
            var currentPath = window.location.href
            if (currentPath.indexOf("cart") != -1){ // position of "cart" string
            refreshCart()
            }
        },
        error: function(errorData){
        $.alert({
            title: "Wait!",
            content: "An error occured",
            theme: "modern",
        })
        }
    })
    })
    // Refresh cart
    function refreshCart(){
    var cartTable = $(".cart-table")
    var cartBody = cartTable.find(".cart-body")
    var productsRows = cartBody.find(".cart-product")
    var currentUrl = window.location.href
    var refreshCartUrl = 'api/cart/'
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax ({
        url: refreshCartUrl,
        method: refreshCartMethod,
        data: data,
        success: function(data) {
        var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
        if (data.products.length > 0) {
            console.log("success")
            productsRows.html("")
            i = data.products.length
            $.each(data.products, function(index, value){
            var newCartItemRemove = hiddenCartItemRemoveForm.clone()
            newCartItemRemove.css("display", "block")
            newCartItemRemove.find(".cart-item-product-id").val(value.id)
            cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + "</td><td>" + value.price + " $" + "<div class='float-right'>" + newCartItemRemove.html() + "</div>" + "</td></tr>")
            i --
            })
            cartBody.find(".cart-total").text(data.total)
        } else {
            window.location.href = currentUrl
        }
        },
        error: function(errorData){
        $.alert({
            title: "Wait!",
            content: "An error occured",
            theme: "modern",
        })
        }
    })

    }
})
