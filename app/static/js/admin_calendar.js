function firstDay(month,year){
    let date = new Date(year,month - 1,1);

    return date.getDay();
}

function getMonthName(month){
    const options = { month: 'long' };
    let date = new Date(1,month - 1)
    return new Intl.DateTimeFormat('en-US',options).format(date);
}


function daysInMonth(month,year){
    let date = new Date(year,month,0);
    return date.getDate();
}

function updateCalendar(){
    // var month = document.getElementById('input_month').value;
    // var year = document.getElementById('input_year').value;
    console.log("month: " + month);
    console.log("year: " + year);

    calendarTable = document.getElementById("calendar");

    let calendarTableContents = '';

    daysOfTheWeek = ["Sunday","Monday","Tuesday", "Wednesday","Thursday","Friday","Saturday"];
    let header = formatTableLine(daysOfTheWeek,true,"");
    console.log(header);

    let firstDayNumber = firstDay(month,year);
    let dayCount = daysInMonth(month,year);

    let monthArrayObject = monthArray(firstDayNumber,dayCount);
    calendarTableContents = header;

    for (let week = 0; week < monthArrayObject.length;week++){
        calendarTableContents += formatTableLine(monthArrayObject[week],false,"calendarItem");
    }

    calendarTable.innerHTML = calendarTableContents;

    let calendarHeader = document.getElementById("month_year");
    calendarHeader.innerHTML = getMonthName(month) + " " + year;
    
    let calendarDays = document.getElementsByClassName("calendarItem");

    for (let day = 0; day < calendarDays.length; day++) {
        calendarDays[day].addEventListener("click", daySelect);
    }

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

function formatTableLine(array,isHeader, insertClass){
    if(insertClass == undefined){
        insertClass = "";
    }
    let tag = "<td";
    let tagClose = "</td>";

    if(isHeader) {
        tag = "<th";
        tagClose = "</th>";
    }

    let line = "<tr>";

    for(let item = 0;item < array.length;item++){
        //line += tag + f"id = ''" +array[item] + tagClose;
        line += `${tag} id='${array[item]}' class='${insertClass}'> ${array[item]} ${tagClose}`
    }

    line += "</tr>"

    return line;
}

function updateMonthYear(changeMonth){
  // changeMonth is only expected to be -1, 0, or 1
  if (changeMonth == 0){
    month = presentMonth;
    year = presentYear;
  }
  else if (month == 1 && changeMonth == -1){
    month = 12;
    year -= 1;
  }
  else if (month == 12 && changeMonth == +1){
    month = 1;
    year += 1;
  }
  else {
    month += changeMonth;
  }
  updateCalendar()
}

var today = new Date();
var presentMonth = today.getMonth() + 1;
var presentYear = today.getFullYear();

var month = presentMonth;
var year = presentYear;
updateCalendar(0)
document.getElementById("pastMonth").addEventListener("click", function(e){updateMonthYear(-1)});
document.getElementById("currentMonth").addEventListener("click", function(e){updateMonthYear(0)});
document.getElementById("nextMonth").addEventListener("click", function(e){updateMonthYear(1)});

let highlightedDay = "1";

function daySelect(event){
    document.getElementById(highlightedDay).style.backgroundColor = "white";
    highlightedDay = (event.target.id);
    console.log(highlightedDay);
    document.getElementById(highlightedDay).style.backgroundColor = "yellow";
    monthData = monthSchedule(year,month)["schedule"];
    console.log(monthData);
    console.log(monthData[parseInt(highlightedDay)]);
    document.getElementById("schedule").innerHTML = dayScheduleFormatter(monthData[parseInt(highlightedDay) - 1]);
}


function dayScheduleFormatter(day_JSON) {
    tableData = formatTableLine(["Period", "Teacher/Info"], true);
    for(const key in day_JSON){
        tableData += formatTableLine([key,day_JSON[key]],false);
    }
    console.log(day_JSON)
    return tableData;
}

function monthSchedule(in_year,in_month){
    for (const x of calendarSchedule){
        if (x.month == in_month.toString() && x.year == in_year.toString()){
            //console.log(x)
            return x;
        }
    }

    return null;
}

defaultTimePeriods = ["First Period", "Second Period", "Third Period", "Fourth Period", "Fifth Period",
    "Sixth Period", "Seventh Period", "Eigth Period", "Ninth Period", "Tenth Period", "After School"];

function defaultDailyTableSet(){
    timePeriods = defaultTimePeriods;

    tableInner = formatTableLine(["Period", "Teacher/Info"], true);
    for(let timePeriod = 0; timePeriod < timePeriods.length;timePeriod++){
        userSelect = `<input type="text" id="box${timePeriod}">`;
        line = formatTableLine(
            [timePeriods[timePeriod],userSelect],
            false
        );
        tableInner += line;
    }

    document.getElementById("defaultScheduleEdit").innerHTML = tableInner;
    

}

function compileEditInfo(tableID,timePeriods){
    table = document.getElementById(tableID);
    scheduleDictionary = {};
    for(let timePeriod = 0; timePeriod < timePeriods.length;timePeriod++){
        textBox = document.getElementById(`box${timePeriod}`)
        scheduleDictionary[timePeriods[timePeriod]] = textBox.value;
    }

    return scheduleDictionary;
}