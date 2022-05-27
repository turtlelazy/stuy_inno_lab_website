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

function updateCalendar(){
    var month = document.getElementById('input_month').value;
    var year = document.getElementById('input_year').value;
    console.log(month);
    console.log(year);

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
    let tag = "<td>";
    let tagClose = "</td>";

    if(isHeader) {
        tag = "<th>";
        tagClose = "</th>";
    }

    let line = "<tr>";

    for(let item = 0;item < array.length;item++){
        line += tag + array[item] + tagClose;
    }

    line += "</tr>"

    return line;
}
