const test = document.getElementsByClassName("message")[0];

// This handler will be executed every time the cursor
// is moved over a different list item
test.addEventListener(
  "mouseover",
  (event) => {
    console.log("mouse over 2");
  },
  false,
);
