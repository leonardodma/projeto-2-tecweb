// // function hover_heart(id){
// //   console.log(id);
// //   document.getElementById(`like-button-${id}`).classList.toggle('liked');
// // }
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.querySelectorAll(".like-button").forEach((element) =>
  element.addEventListener("click", (e) => {
    e.currentTarget.classList.toggle("liked");

    const csrftoken = getCookie("csrftoken");

    data = e.currentTarget.dataset.id;

    fetch(`/api/adoptions/${data}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    });
  })
);


document.querySelectorAll(".like-button2").forEach((element) =>
  element.addEventListener("click", (e) => {
    e.currentTarget.classList.toggle("liked");

    const csrftoken = getCookie("csrftoken");

    data = e.currentTarget.dataset.id;

    fetch(`/api/adoptions/${data}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    });
  })
);


if(!!window.performance && window.performance.navigation.type == 2)
{
    window.location.reload();
}