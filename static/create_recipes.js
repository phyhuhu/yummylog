const $add_food_ingredients = $('#add_food_ingredients');
const $add_food_instructions = $('#add_food_instructions');
const $add_drink_ingredients = $('#add_drink_ingredients');
const $add_drink_instructions = $('#add_drink_instructions');

$('#a_food_ingredients').on("click", function(evt) {
    evt.preventDefault(); // no page refresh

    for (let i=0; i<$add_food_ingredients.find('div').length; i++) { 
        if ($add_food_ingredients.find('div')[i].style[0]) {
            $add_food_ingredients.find('div')[i].style="";
            break;
        }
    }
});

$('#r_food_ingredients').on("click", function(evt) {
    evt.preventDefault(); // no page refresh

    let pos=$add_food_ingredients.find('div').length;
    for (let i=0; i<$add_food_ingredients.find('div').length; i++) { 
        if ($add_food_ingredients.find('div')[i].style[0]) {
            pos=i;
            break;
        }
    }
    if (pos>1){
        $add_food_ingredients.find('div')[pos-1].style="display:none;";
    }
});

$('#a_food_instructions').on("click", function(evt) {
    evt.preventDefault(); // no page refresh

    for (let i=0; i<$add_food_instructions.find('div').length; i++) { 
        if ($add_food_instructions.find('div')[i].style[0]) {
            $add_food_instructions.find('div')[i].style="";
            break;
        }
    }
});

$('#r_food_instructions').on("click", function(evt) {
    evt.preventDefault(); // no page refresh

    let pos=$add_food_instructions.find('div').length;
    for (let i=0; i<$add_food_instructions.find('div').length; i++) { 
        if ($add_food_instructions.find('div')[i].style[0]) {
            pos=i;
            break;
        }
    }
    if (pos>1){
        $add_food_instructions.find('div')[pos-1].style="display:none;";
    }
});

$('#a_drink_ingredients').on("click", function(evt) {
    evt.preventDefault(); // no page refresh

    for (let i=0; i<$add_drink_ingredients.find('div').length; i++) { 
        if ($add_drink_ingredients.find('div')[i].style[0]) {
            $add_drink_ingredients.find('div')[i].style="";
            break;
        }
    }
});

$('#r_drink_ingredients').on("click", function(evt) {
    evt.preventDefault(); // no page refresh

    let pos=$add_drink_ingredients.find('div').length;
    for (let i=0; i<$add_drink_ingredients.find('div').length; i++) { 
        if ($add_drink_ingredients.find('div')[i].style[0]) {
            pos=i;
            break;
        }
    }
    if (pos>1){
        $add_drink_ingredients.find('div')[pos-1].style="display:none;";
    }
});

$('#a_drink_instructions').on("click", function(evt) {
    evt.preventDefault(); // no page refresh

    for (let i=0; i<$add_drink_instructions.find('div').length; i++) { 
        if ($add_drink_instructions.find('div')[i].style[0]) {
            $add_drink_instructions.find('div')[i].style="";
            break;
        }
    }
});

$('#r_drink_instructions').on("click", function(evt) {
    evt.preventDefault(); // no page refresh

    let pos=$add_drink_instructions.find('div').length;
    for (let i=0; i<$add_drink_instructions.find('div').length; i++) { 
        if ($add_drink_instructions.find('div')[i].style[0]) {
            pos=i;
            break;
        }
    }
    if (pos>1){
        $add_drink_instructions.find('div')[pos-1].style="display:none;";
    }
});