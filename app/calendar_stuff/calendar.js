function firstDay(month,year){
    let date = new Date(year,month - 1,1);

    return date.getDay();
}

function getMonth(month){
    const options = { month: 'long' };
    let date = new Date(1,month - 1)
    return new Intl.DateTimeFormat('en-US',options).format(date);
}

function daysInMonth(month,year){
    let date = new Date(year,month,0);
    return date.getDate();
}

function updateCalendar(month,year){
    calendarTable = document.getElementById("calendar");

    let calendarTableContents = '';
    
    daysOfTheWeek = ["Sunday","Monday","Tuesday", "Wednesday","Thursday","Friday","Saturday"];
    let header = formatTableLine(daysOfTheWeek,true);
    console.log(header);

    let firstDayNumber = firstDay(month,year);
    let dayCount = daysInMonth(month,year);


    let monthArrayObject = monthArray(firstDayNumber,dayCount);
    calendarTableContents = header;

    for (let week = 0; week < monthArrayObject.length;week++){
        calendarTableContents += formatTableLine(monthArrayObject[week]);
    }

    calendarTable.innerHTML = calendarTableContents;

    let calendarHeader = document.getElementById("month");
    calendarHeader.innerHTML = getMonth(month);
}

function weekArray(sundayStart,maxDate){

    let returnArray = new Array(7);
    for (let day = 0; day < 7  ; day++ ){
        if (day + sundayStart >= 0 && day + sundayStart + 1 <= maxDate){
            returnArray[day] = day + sundayStart + 1;
        }
        else{
            returnArray[day] = ""
        }
    }

    return returnArray;
}

function monthArray(firstDay,dayCount){
    let monthArray = [];

    for(let week = 0; week < 6; week++){
        monthArray.push(weekArray(-firstDay + week * 7,dayCount))
    }
    return monthArray;
}

function formatTableLine(array,isHeader){
    let tag = "<td";
    let tagClose = "</td>";

    if(isHeader) {
        tag = "<th";
        tagClose = "</th>";
    }

    let line = "<tr>";

    for(let item = 0;item < array.length;item++){
        //line += tag + f"id = ''" +array[item] + tagClose;
        line += `${tag} id='${array[item]}'> ${array[item]} ${tagClose}`
    }

    line += "</tr>"

    return line;
}


let test_data = [];

for(let i = 1; i < 32; i++){
    let test_day_JSON = {
        "first_period":"None",
        "second_period":"Scott Thomas",
        "third_period":"Someone Else",
        "fourth_period":"None",
        "fifth_period":"None",
        "sixth_period":"Joseph Blay",
        "seventh_period":"Joseph Blay",
        "eight_period":"Scott Thomas",
        "ninth_period":"None",
        "tenth_period":"Scott Thomas",
        "after_school":{"teacher":"Scott Thomas","time":i%3}
    }
    
    test_data.push(test_day_JSON);
}