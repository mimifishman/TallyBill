document.addEventListener("DOMContentLoaded", function () {
  // check if bill is loaded
  if (document.getElementById("bill") != undefined) {
    // get the bill id
    var bill_id = document.getElementById("bill_id").innerHTML;

    // hide the error bar
    document.getElementById("json-error_div").style.display = "none";

    // get the CSRF token
    csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // add event listener to the share button
    document.getElementById("share").addEventListener("click", () => {
      const title = document.title;
      const text = "Join my bill on TallyBill!";
      const url = window.location.href;
      // check if the user browser can share, if not use email.
      if (navigator.share !== undefined) {
        navigator
          .share({
            title,
            text,
            url,
          })
          .catch((err) => show_json_errors(err));
      } else {
        window.location = `mailto:?subject=${title}&body=${text}%0A${url}`;
      }
    });

    //load the bill lines
    get_bill_lines(bill_id);
    //load the bill people
    get_bill_users(bill_id);

    // change the icon of the toggle detail header
    var header_details = document.getElementById("header_details");
    var chevron_image = document.getElementById("chevron-image");
    header_details.addEventListener("show.bs.collapse", function () {
      chevron_image.src = "../static/tally/images/chevron-double-left.svg";
    });
    header_details.addEventListener("hide.bs.collapse", function () {
      chevron_image.src = "../static/tally/images/chevron-double-right.svg";
    });

    // Show the line item form modal
    document.getElementById("add_line").addEventListener("click", () => {
      document.getElementById("line_modal_title").innerHTML = "Add Item";
      $("#line_modal").modal("show");
    });

    // add an event listener to the item form submit
    document
      .getElementById("line_form_modal")
      .addEventListener("submit", () => {
        let line_id = document.getElementById("id_line").value;
        if (line_id == 0) {
          new_bill_line(bill_id);
        } else {
          line_update(line_id);
        }
        $("#line_modal").modal("hide");
      });

    // clear the line form when the  line model is hidden
    $("#line_modal").on("hidden.bs.modal", function () {
      document.getElementById("line_form_modal").reset();
      document.getElementById("id_line").value = 0;
    });

    // Show the user form modal
    document.getElementById("add_user").addEventListener("click", () => {
      document.getElementById("user_modal_title").innerHTML = "Add Person";
      $("#user_modal").modal("show");
    });

    // add an event listener to the user form submit
    document
      .getElementById("user_form_modal")
      .addEventListener("submit", () => {
        let user_id = document.getElementById("id_user").value;
        if (user_id == 0) {
          add_bill_users(bill_id);
        } else {
          update_bill_user(user_id);
        }
        $("#user_modal").modal("hide");
      });

    // add event listener to the user delete button
    document.getElementById("btn_user_del").addEventListener("click", () => {
      //update the user on the delete modal and show the model
      document.getElementById("delete_modal_id").innerHTML =
        document.getElementById("id_user").value;
      document.getElementById("delete_modal_type").innerHTML = "user";
      document.getElementById("delete-modal-text").innerHTML =
        "Are you sure you want to delete the person?";
      $("#user_modal").modal("hide");
      $("#delete-modal").modal("show");
    });

    // clear the user form on line model hidden
    $("#user_modal").on("hidden.bs.modal", function () {
      document.getElementById("user_form_modal").reset();
      document.getElementById("id_user").value = 0;
      document.getElementById("btn_user_del").style.visibility = "hidden";
    });

    // add event listener to main show/hide people
    let ppl_show_main = document.getElementById("people_show_main");
    let ppl_symbol = document.getElementById("people_collapse_main");
    ppl_show_main.addEventListener("click", function () {
      if (ppl_symbol.innerHTML == "-") {
        ppl_symbol.innerHTML = "+";
      } else {
        ppl_symbol.innerHTML = "-";
      }
    });

    // add on event listener to the total bill to display the totals
    document.getElementById("total_bill").addEventListener("click", () => {
      // don't allow edit the header on the totals view
      document.getElementById("edit_header").style.display = "none";
      document.getElementById("bill_details").style.display = "none";
      get_bill_totals(bill_id);
      document.getElementById("bill_totals").style.display = "block";
    });
    // add an event listener to hide the totals and show the main bill
    document
      .getElementById("show_bill_details")
      .addEventListener("click", () => {
        //allow edit the header on the totals view
        document.getElementById("edit_header").style.display = "block";
        document.getElementById("bill_details").style.display = "block";
        document.getElementById("bill_totals").style.display = "none";
      });
  }

  // check if not the header view and create observers
  if (document.getElementById("bill_id")) {
    // add a mutatation observer to update the bill users count
    var bill_users = document.getElementById("user_list");
    const mutationObserverUsers = new MutationObserver(() => {
      let count_users = bill_users.querySelectorAll("#btn_user").length;
      document.querySelector("#bill_users_total").innerHTML = count_users;
    });
    mutationObserverUsers.observe(bill_users, {
      subtree: true,
      childList: true,
      attributes: true,
    });

    // add a mutatation observer to item line to update the total bill
    var table = document.getElementById("table-lines");
    const mutationObserverLineItem = new MutationObserver(() => {
      var sum_value = 0;
      Array.from(table.rows).forEach((row) => {
        if (row.cells[2]) {
          sum_value += Number(
            row.cells[2].innerHTML.replace(String.fromCharCode(36), "")
          );
        }
      });
      document.getElementById("total_bill").innerHTML =
        "Total: " +
        String.fromCharCode(36) +
        Intl.NumberFormat().format(sum_value);
    });
    mutationObserverLineItem.observe(table, {
      subtree: true,
      childList: true,
      attributes: true,
    });
  }

  // focus on the first input on the model form
  $(".modal").on("shown.bs.modal", function () {
    $(this).find("input:visible:first").focus();
  });

  // add event listeners to the delete modal
  document
    .getElementById("delete-modal-btn-del")
    .addEventListener("click", () => {
      let id = document.getElementById("delete_modal_id").innerHTML;
      let type = document.getElementById("delete_modal_type").innerHTML;
      if (type == "item") {
        //delete the item;
        line_delete(id);
      } else if (type == "user") {
        //delete the user
        delete_bill_user(id);
      } else {
        alert("Delete type error.");
      }
    });

  // clear the delete model on hidden
  $("#delete_modal").on("hidden.bs.modal", function () {
    document.getElementById("delete_modal_id").innerHTML = 0;
    document.getElementById("delete_modal_type").innerHTML = "";
  });
});

// show the json errors
function show_json_errors(error) {
  document.getElementById("json-error_div").style.display = "block";
  document.getElementById("json_error").innerHTML = error;
}

/*----------------------------------------------------------------------------- START BILL LINE--------------------------------------------------------*/
// create the line table row
function create_row(line) {
  // /create the html table of items
  let tableBody = document.getElementById("tbody-lines");
  var row = tableBody.insertRow(-1);
  let cell0 = row.insertCell(0);
  let cell1 = row.insertCell(1);
  let cell2 = row.insertCell(2);
  let cell3 = row.insertCell(3);
  let cell4 = row.insertCell(4);

  // add class and attributes to the table row
  row.classList.add("align-self-start");
  row.setAttribute("height", "50px");
  cell2.classList.add("text-end");
  // add a dataset to the table row
  row.setAttribute("data-item", line.line_id);

  // set the cells HTML
  cell0.innerHTML = line.item;
  cell1.innerHTML = line.quantity;
  cell2.innerHTML = String.fromCharCode(36) + Number(line.total).toFixed(2);
  cell3.innerHTML = `<div  class="text-end"><button id="all_users" class="xs-circle">All</button>  &nbsp
                        <a id="people_show" class="text-decoration-none">
                            <img src="../static/tally/images/people.svg" alt="People" role=button  width="20" height="20" ><span id='people-collapse' class="text-primary">+</span>        
                        </a>
                        </div>`;
  cell4.innerHTML = `<div  class="text-end"> <img src="../static/tally/images/edit.svg" alt="Edit"  id="edit_line" role=button width="20" height="20" class="me-3">
        <img src="../static/tally/images/trash.svg" alt="Delete" id="delete_line" role=button  width="20" height="20"> </div>`;

  // create a row for the line users
  var row_users = tableBody.insertRow(-1);
  let cell0_users = row_users.insertCell(0);
  cell0_users.setAttribute("colspan", "12");
  row_users.setAttribute("data-item-users", line.line_id);
  row_users.id = "item_users_" + line.line_id;
  row_users.classList.add("collapse", "multi-collapse", "align-top");

  // create toggle for the line users
  ppl_btn = row.querySelector("#people_show");
  ppl_btn.setAttribute("data-bs-toggle", "collapse");
  ppl_btn.setAttribute("href", "#" + row_users.id);

  row_users.addEventListener("show.bs.collapse", function () {
    row.querySelector("#people-collapse").innerHTML = "-";
  });

  row_users.addEventListener("hidden.bs.collapse", function () {
    row.querySelector("#people-collapse").innerHTML = "+";
  });

  // line users count
  var line_users_count = document.createElement("TAG");
  line_users_count.innerHTML = 0;
  line_users_count.classList.add("d-none");
  line_users_count.id = "line_users_count";
  row.append(line_users_count);

  // add a mutatation observer to user rows to update the line user count
  const mutationObserverLineUser = new MutationObserver(() => {
    let count = 0;
    btn_line_user = row_users.querySelectorAll("#btn_user_line");
    btn_line_user.forEach((user) => {
      // check if the users with color in the row to see which user is attached to the row
      if (user.style.background != "grey") {
        count += 1;
      }
      line_users_count.innerHTML = count;
      // update the count of users on the row
      if (
        line_users_count.innerHTML ==
        document.getElementById("bill_users_total").innerHTML
      ) {
        row.querySelector("#all_users").style.background = "#e95420";
      } else {
        row.querySelector("#all_users").style.background = "grey";
      }
    });
  });
  mutationObserverLineUser.observe(row_users, {
    subtree: true,
    childList: true,
    attributes: true,
  });

  //show the line users
  get_bill_line_users(line);

  // add an event listener to the All button to add or remove all users
  //0 user id removes or adds all users
  row.querySelector("#all_users").addEventListener("click", () => {
    add_line_user(line.line_id, 0);
  });

  // add an event listener to the line edit button
  row
    .querySelector("#edit_line")
    .addEventListener("click", () => line_edit(line.line_id));

  // add an event listener to the line delete button
  row.querySelector("#delete_line").addEventListener("click", () => {
    //update the line id on the delete modal and show the model
    document.getElementById("delete_modal_id").innerHTML = line.line_id;
    document.getElementById("delete_modal_type").innerHTML = "item";
    document.getElementById("delete-modal-text").innerHTML =
      "Are you sure you want to delete the item?";
    $("#delete-modal").modal("show");
  });
}

// show the bill lines
function get_bill_lines(bill_id) {
  // fetch the bill line items
  fetch("/bill_view_json/" + bill_id)
    .then((response) => response.json())
    .then((lines) => {
      try {
        if (lines.error) {
          show_json_errors(lines.error);
        } else {
          lines.forEach((line) => {
            //create a line item in the table
            create_row(line);
          });
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// Create new bill line
function new_bill_line(bill_id) {
  fetch("/line_json/" + bill_id, {
    method: "POST",
    body: JSON.stringify({
      item: document.getElementById("id_item").value,
      total: document.getElementById("id_total").value,
      quantity: document.getElementById("id_quantity").value,
      line_id: document.getElementById("id_line").value,
    }),
    headers: { "X-CSRFToken": csrftoken },
    mode: "same-origin", // Do not send CSRF token to another domain.
  })
    .then((response) => response.json())
    .then((line) => {
      try {
        if (line.error) {
          show_json_errors(line.error);
        } else {
          // Add the new row to the table
          let table = document.getElementById("table-lines");
          // go to the new row
          let last_row = table.rows.length - 1;
          // check if there are no rows
          if (last_row >= 0) {
            table.rows[last_row].scrollIntoView({ behavior: "smooth" });
          }
          create_row(line);
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// edit the bill line
function line_edit(line_id) {
  // get the line
  fetch("/edit_line_json/" + line_id)
    .then((response) => response.json())
    .then((line) => {
      try {
        if (line.error) {
          show_json_errors(line.error);
        } else {
          //Show the form
          document.getElementById("line_modal_title").innerHTML = "Update Item";
          $("#line_modal").modal("show");
          // fill out the form fields.
          document.getElementById("id_item").value = line.item;
          document.getElementById("id_total").value = line.total;
          document.getElementById("id_quantity").value = line.quantity;
          document.getElementById("id_line").value = line.line_id;
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// Update the bill line
function line_update(line_id) {
  fetch("/edit_line_json/" + line_id, {
    method: "PUT",
    body: JSON.stringify({
      item: document.getElementById("id_item").value,
      total: document.getElementById("id_total").value,
      quantity: document.getElementById("id_quantity").value,
      line_id: document.getElementById("id_line").value,
    }),
    headers: { "X-CSRFToken": csrftoken },
    mode: "same-origin", // Do not send CSRF token to another domain.
  })
    .then((response) => response.json())
    .then((line) => {
      try {
        if (line.error) {
          show_json_errors(line.error);
        } else {
          // get the table row
          const row = document.querySelector(`tr[data-item="${line.line_id}"]`);
          //update the table row data
          row.cells[0].innerHTML = line.item;
          row.cells[1].innerHTML = line.quantity;
          row.cells[2].innerHTML =
            String.fromCharCode(36) + Number(line.total).toFixed(2);
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// delete the bill line
function line_delete(line_id) {
  fetch("/edit_line_json/" + line_id, {
    method: "DELETE",
    body: JSON.stringify({
      line_id: line_id,
    }),
    headers: { "X-CSRFToken": csrftoken },
    mode: "same-origin", // Do not send CSRF token to another domain.
  })
    .then((response) => response.json())
    .then((line) => {
      try {
        if (line.error) {
          show_json_errors(line.error);
        } else {
          // get the table rows
          let row = document.querySelector(`tr[data-item="${line_id}"]`);
          let row_user = document.querySelector(
            `tr[data-item-users="${line_id}"]`
          );
          //remove the table rows
          document.getElementById("table-lines").deleteRow(row.rowIndex);
          document.getElementById("table-lines").deleteRow(row_user.rowIndex);
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

/*------------------------------------------------------------------- END BILL LINE---------------------------------------------------------------------*/

/* ------------------------------------------------------------------ START BILL USER----------------------------------------------------------------- */
// add or remove user from line and change button color
function add_line_user(line_id, user_id) {
  fetch("/add_line_user/" + line_id, {
    method: "POST",
    body: JSON.stringify({
      user_id: user_id,
    }),
    headers: { "X-CSRFToken": csrftoken },
    mode: "same-origin", // Do not send CSRF token to another domain.
  })
    .then((response) => response.json())
    .then((users) => {
      try {
        if (users.error) {
          show_json_errors(users.error);
        } else {
          users.forEach((user) => {
            row = document.querySelector(`[data-item-users="${line_id}"]`);
            person = row.querySelector(`[data-user="${user.user_id}"]`);
            if (user.type == "add") {
              person.style.background = user.color;
            } else if (user.type == "remove") {
              person.style.background = "grey";
            }
          });
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// create the line user
function create_line_user_button(id, name, color, line_id) {
  let btn_user = document.createElement("BUTTON");
  btn_user.setAttribute("data-user", id);
  btn_user.classList.add("small-circle");
  btn_user.id = "btn_user_line";
  btn_user.innerHTML = name;
  btn_user.style.background = color;
  // add button event listener
  btn_user.addEventListener("click", () => add_line_user(line_id, id));
  // append the button
  row = document.querySelector(`tr[data-item-users="${line_id}"]`);
  row.cells[0].append(btn_user);
}

// show bill line users
function get_bill_line_users(line) {
  // get the bill users
  fetch("/bill_users_json/" + line.bill_id)
    .then((response) => response.json())
    .then((users) => {
      try {
        if (users.error) {
          show_json_errors(users.error);
        } else {
          users.forEach((user) => {
            // check if the user was added to the line and change the color
            if (line.line_users.includes(user.user_id)) {
              var color = user.color;
            } else {
              color = "grey";
            }
            //create a user line button
            create_line_user_button(
              user.user_id,
              user.name,
              color,
              line.line_id
            );
          });
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// create the user button
function create_user_button(id, name, color) {
  let btn_user = document.createElement("BUTTON");
  btn_user.setAttribute("data-user", id);
  btn_user.classList.add("large-circle");
  btn_user.id = "btn_user";
  btn_user.innerHTML = name;
  btn_user.style.background = color;
  let add_user = document.getElementById("add_user");
  document.getElementById("user_list").insertBefore(btn_user, add_user);

  // add an eventlistener to the button
  btn_user.addEventListener("click", () => edit_bill_user(id));
}

// show bill users
function get_bill_users(bill_id) {
  // get the bill users
  fetch("/bill_users_json/" + bill_id)
    .then((response) => response.json())
    .then((users) => {
      try {
        if (users.error) {
          show_json_errors(users.error);
        } else {
          users.forEach((user) => {
            //create a user button
            create_user_button(user.user_id, user.name, user.color);
          });
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// Add a bill user
function add_bill_users(bill_id) {
  fetch("/bill_users_json/" + bill_id, {
    method: "POST",
    body: JSON.stringify({
      name: document.getElementById("id_name").value,
      tip: document.getElementById("id_tip").value,
    }),
    headers: { "X-CSRFToken": csrftoken },
    mode: "same-origin", // Do not send CSRF token to another domain.
  })
    .then((response) => response.json())
    .then((user) => {
      try {
        if (user.error) {
          show_json_errors(users.error);
        } else {
          //create a user button
          create_user_button(user.user_id, user.name, user.color);

          // creates the lines user button
          rows = document.querySelectorAll("[data-item-users]");
          rows.forEach((row) => {
            line_id = row.getAttribute("data-item-users");
            create_line_user_button(user.user_id, user.name, "grey", line_id);
          });
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// edit bill user
function edit_bill_user(user_id) {
  // get the user
  fetch("/edit_user_json/" + user_id)
    .then((response) => response.json())
    .then((user) => {
      try {
        if (user.error) {
          show_json_errors(user.error);
        } else {
          document.getElementById("id_name").value = user.name;
          document.getElementById("id_tip").value = user.tip;
          document.getElementById("id_user").value = user.user_id;
          document.getElementById("btn_user_del").style.visibility = "visible";
          document.getElementById("user_modal_title").innerHTML =
            "Update Person";
          $("#user_modal").modal("show");
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// update bill user
function update_bill_user(user_id) {
  fetch("/edit_user_json/" + user_id, {
    method: "PUT",
    body: JSON.stringify({
      name: document.getElementById("id_name").value,
      tip: document.getElementById("id_tip").value,
      user_id: document.getElementById("id_user").value,
    }),
    headers: { "X-CSRFToken": csrftoken },
    mode: "same-origin", // Do not send CSRF token to another domain.
  })
    .then((response) => response.json())
    .then((user) => {
      try {
        if (user.error) {
          show_json_errors(user.error);
        } else {
          //Update the user button
          let person = document.querySelectorAll(
            `[data-user="${user.user_id}"]`
          );
          person.forEach((p) => {
            p.innerHTML = user.name;
          });
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

// delete bill user
function delete_bill_user(user_id) {
  fetch("/edit_user_json/" + user_id, {
    method: "DELETE",
    body: JSON.stringify({
      user_id: user_id,
    }),
    headers: { "X-CSRFToken": csrftoken },
    mode: "same-origin", // Do not send CSRF token to another domain.
  })
    .then((response) => response.json())
    .then((user) => {
      try {
        if (user.error) {
          show_json_errors(user.error);
        } else {
          let person = document.querySelectorAll(`[data-user="${user_id}"]`);
          person.forEach((p) => {
            p.remove();
          });
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}

/* ------------------------------------------------------------END BILL USER-----------------------------------------------------------------------------------*/

/*------------------------------------------------------- Bill Totals---------------------------------------------------------------------- */
// get the bill totals
function get_bill_totals(bill_id) {
  // fetch the bill totals
  fetch("/bill_totals/" + bill_id)
    .then((response) => response.json())
    .then((totals) => {
      try {
        if (totals.error) {
          show_json_errors(lines.error);
        } else {
          // totals for each user
          var bill_totals_user_el = document.getElementById("bill_totals_user");
          bill_totals_user_el.innerHTML = "";
          var total_bill_tip = 0;

          var main_user_el = document.createElement("div");
          bill_totals_user_el.append(main_user_el);

          totals.users.forEach((total) => {
            // user subtotals
            const subtotals = [];
            var items_subtotal = parseFloat(total.total_items_cost);
            var tip_value = parseFloat(total.total_items_tip).toFixed(2);
            var tax_subtotal = parseFloat(
              items_subtotal * (1 + total.tax / 100)
            ).toFixed(2);
            var tip_subtotal = parseFloat(
              parseFloat(tax_subtotal) + parseFloat(tip_value)
            ).toFixed(2);
            subtotals.push(
              { type: "items_subtotal", value: items_subtotal },
              { type: "tax_subtotal", value: tax_subtotal },
              { type: "tip_value", value: tip_value },
              { type: "tip_subtotal", value: tip_subtotal }
            );

            //total user bill value
            total_bill_tip += parseFloat(tip_value);
            // user totals
            user_el = document.createElement("div");
            user_el.classList.add("d-flex", "mt-2", "mb-0", "pb-0");
            main_user_el.append(user_el);
            name_el = document.createElement("h4");
            name_el.classList.add("col-auto", "text-primary", "mb-0", "pb-0");
            cost_el = document.createElement("h4");
            cost_el.classList.add("ms-auto", "text-primary", "mb-0", "pb-0");
            user_el.append(name_el, cost_el);
            name_el.innerHTML = total.name;
            cost_el.innerHTML = String.fromCharCode(36) + tip_subtotal;

            // user details link
            user_details_el = document.createElement("div");
            user_details_el.classList.add("d-flex", "mb-2");
            user_details_el.id = "show_user_details";
            main_user_el.append(user_details_el);
            details_el = document.createElement("a");
            details_el.classList.add(
              "ms-auto",
              "text-muted",
              "text-decoration-none"
            );
            user_details_el.append(details_el);
            details_el.innerHTML = `<small><span id = user_details_symbol-${total.user_id} > + </span> Details </small>`;
            details_el.setAttribute("data-bs-toggle", "collapse");
            details_el.setAttribute("href", "#user_details-" + total.user_id);

            // Create item div
            var items_el = document.createElement("div");
            items_el.classList.add("ms-4", "collapse");
            items_el.id = "user_details-" + total.user_id;
            main_user_el.append(items_el);

            // change the symbol on user details collapse
            items_el.addEventListener("show.bs.collapse", function () {
              document.querySelector(
                "#user_details_symbol-" + `${total.user_id}`
              ).innerHTML = "-";
            });
            items_el.addEventListener("hidden.bs.collapse", function () {
              document.querySelector(
                "#user_details_symbol-" + `${total.user_id}`
              ).innerHTML = "+";
            });

            //   Get the line items
            total.line_items.forEach((item) => {
              item_el = document.createElement("div");
              item_el.classList.add("d-flex", "flex-wrap", "mb-2");
              items_el.append(item_el);
              name_el = document.createElement("h6");
              name_el.classList.add("col-auto", "mb-0");
              cost_el = document.createElement("h6");
              cost_el.classList.add("ms-auto", "col-auto", "mb-0");
              share_el = document.createElement("small");
              share_el.classList.add("col-12", "text-muted", "mb-0");
              item_el.append(name_el, cost_el, share_el);
              name_el.innerHTML = item.item;
              cost_el.innerHTML = String.fromCharCode(36) + item.user_cost;
              if (item.line_users_names != "") {
                share_el.innerHTML =
                  item.total + " split with " + item.line_users_names;
              } else {
                share_el.innerHTML = item.total + " not split ";
              }
            });

            // subtotals
            subtotals.forEach((subtotal) => {
              var name = "";
              if (subtotal.type == "items_subtotal") {
                name = "Items subtotal";
              } else if (subtotal.type == "tax_subtotal") {
                name = `Tax subtotal <small class="text-muted">${total.tax}%</small>`;
              } else if (subtotal.type == "tip_value") {
                name = `Tip <small class="text-muted">${total.tip}%</small>`;
              } else if (subtotal.type == "tip_subtotal") {
                name = "Total with tip";
              }
              if (!(subtotal.type == "tax_subtotal" && total.tax == 0.0)) {
                subtotal_el = document.createElement("div");
                subtotal_el.classList.add("d-flex", "mb-2");
                items_el.append(subtotal_el);
                name_el = document.createElement("h6");
                name_el.classList.add("col-auto");
                cost_el = document.createElement("h6");
                cost_el.classList.add("ms-auto", "col-auto");
                if (
                  subtotal.type == "items_subtotal" ||
                  subtotal.type == "tip_subtotal"
                ) {
                  cost_el.classList.add(
                    "border-top",
                    "border-dark",
                    "text-dark"
                  );
                  name_el.classList.add("text-dark");
                }
                subtotal_el.append(name_el, cost_el);
                name_el.innerHTML = name;
                cost_el.innerHTML =
                  String.fromCharCode(36) +
                  parseFloat(subtotal.value).toFixed(2);
              }
            });
          });

          // grand total
          grand_total_el = document.createElement("div");
          grand_total_el.classList.add("d-flex", "mt-3", "mb-0");
          main_user_el.append(grand_total_el);
          name_el = document.createElement("h4");
          name_el.classList.add("col-auto", "text-dark", "mb-0");
          cost_el = document.createElement("h4");
          cost_el.classList.add("ms-auto", "text-dark", "mb-0");
          grand_total_el.append(name_el, cost_el);
          name_el.innerHTML = "Bill Total";
          cost_el.innerHTML =
            String.fromCharCode(36) +
            Intl.NumberFormat().format(
              parseFloat(
                totals.total_lines * (1 + totals.tax / 100) + total_bill_tip
              ).toFixed(2)
            );

          // grand total details link
          totals_details_el = document.createElement("div");
          totals_details_el.classList.add("d-flex", "mb-2");
          totals_details_el.id = "show_total_details";
          main_user_el.append(totals_details_el);
          details_el = document.createElement("a");
          details_el.classList.add(
            "ms-auto",
            "text-muted",
            "text-decoration-none"
          );
          totals_details_el.append(details_el);
          details_el.innerHTML = `<small><span id = total_details_symbol> + </span> Details </small>`;
          details_el.setAttribute("data-bs-toggle", "collapse");
          details_el.setAttribute("href", "#total_details");

          // grand total details
          var totals_el = document.createElement("div");
          totals_el.classList.add("ms-4", "collapse");
          totals_el.id = "total_details";
          main_user_el.append(totals_el);

          // change the symbol on grand total details collapse
          totals_el.addEventListener("show.bs.collapse", function () {
            document.querySelector("#total_details_symbol").innerHTML = "-";
          });
          totals_el.addEventListener("hidden.bs.collapse", function () {
            document.querySelector("#total_details_symbol").innerHTML = "+";
          });

          // get the total details
          var totals_details = [];

          totals_details.push(
            { type: "bill_items_subtotal", value: totals.total_lines },
            { type: "people_items_subtotal", value: totals.user_line_total },
            {
              type: "unallocated_items",
              value: totals.total_lines - totals.user_line_total,
            },
            {
              type: "tax_subtotal",
              value: totals.total_lines * (1 + totals.tax / 100),
            },
            { type: "tip_value", value: totals.user_tip_total },
            {
              type: "tip_subtotal",
              value:
                parseFloat(totals.total_lines * (1 + totals.tax / 100)) +
                parseFloat(totals.user_tip_total),
            }
          );

          totals_details.forEach((total) => {
            var name = "";
            if (total.type == "bill_items_subtotal") {
              name = "Bill items subtotal";
            } else if (total.type == "people_items_subtotal") {
              name = "People items subtotal";
            } else if (total.type == "unallocated_items") {
              name = "Unallocated items";
            } else if (total.type == "tax_subtotal") {
              name = `Tax subtotal <small class="text-muted">${totals.tax}%</small>`;
            } else if (total.type == "tip_value") {
              name = `Tip <small class="text-muted">${totals.user_avg_tip}% (avg.)</small>`;
            } else if (total.type == "tip_subtotal") {
              name = "Total with tip";
            }

            // add the grand total details
            if (!(total.type == "tax_subtotal" && totals.tax == 0.0)) {
              totals_subtotal_el = document.createElement("div");
              totals_subtotal_el.classList.add("d-flex", "mb-2", "fw-bolder");
              totals_el.append(totals_subtotal_el);
              name_el = document.createElement("h6");
              name_el.classList.add("col-auto");
              cost_el = document.createElement("h6");
              cost_el.classList.add("ms-auto", "col-auto");
              if (
                total.type == "unallocated_items" ||
                total.type == "tip_subtotal"
              ) {
                cost_el.classList.add("border-top", "border-dark", "text-dark");
                name_el.classList.add("text-dark");
              }
              totals_subtotal_el.append(name_el, cost_el);
              name_el.innerHTML = name;
              cost_el.innerHTML =
                String.fromCharCode(36) + parseFloat(total.value).toFixed(2);
            }
          });
        }
      } catch (err) {
        show_json_errors(err);
      }
    });
  return false;
}
/* ------------------------------------------------------------End Bill Totals---------------------------------------------------------------------- */
