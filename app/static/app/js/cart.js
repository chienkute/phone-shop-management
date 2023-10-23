var updateBtns = document.getElementsByClassName("update-cart");

// vòng lặp qua từng phaanft tử , với mỗi nút click sẽ thực hiện hàm xử lý
for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    // lấy các giá trị dữ liệu từ phần tử dc nhấp vào

    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId", productId, "action", action);
    console.log("user", user);
    if (user === "AnonymousUser") {
      console.log("user not loggin");
    } else {
      updateUserOrder(productId, action);
    }
  });
}
function updateUserOrder(productId, action) {
  console.log("user logged in");
  var url = "/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data", data);
      location.reload();
    });
}

// function addToCart(productId) {
//   var url = "/add_to_cart/";
//   var data = {
//     product_id: productId,
//   };
//   var xhr = new XMLHttpRequest();
//   xhr.open("POST", url);
//   xhr.setRequestHeader("Content-Type", "application/json");
//   xhr.onload = function () {
//     if (xhr.status === 200) {
//       var cartItemSpan = document.getElementById("cart-item-" + productId);
//       var cartItemCount = parseInt(cartItemSpan.innerHTML) + 1;
//       cartItemSpan.innerHTML = cartItemCount;
//     }
//   };
//   xhr.send(JSON.stringify(data));
// }
// function removeFromCart(productId) {
//   var url = "/cart/remove_from_cart/";
//   var data = {
//     product_id: productId,
//   };
//   var xhr = new XMLHttpRequest();
//   xhr.open("POST", url);
//   xhr.setRequestHeader("Content-Type", "application/json");
//   xhr.onload = function () {
//     if (xhr.status === 200) {
//       var cartItemSpan = document.getElementById("cart-item-" + productId);
//       var cartItemCount = parseInt(cartItemSpan.innerHTML) - 1;
//       if (cartItemCount < 0) {
//         cartItemCount = 0;
//       }
//       cartItemSpan.innerHTML = cartItemCount;
//     }
//   };
//   xhr.send(JSON.stringify(data));
// }

