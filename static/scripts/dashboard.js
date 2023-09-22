console.log("JavaScript code is being executed!");


// Sidebar Toggle

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

// define open side bar function
function openSidebar(){
    if(!sidebarOpen){
        sidebar.classList.add("sidebar-responsive");
        sidebarOpen = true;
    }
}

// define a close sidebar function
function closeSidebar(){
    if(sidebarOpen){
        sidebar.classList.remove("sidebar-responsive");
        sidebarOpen = false;
    }
}




// define a function to redirect to teams information page
var aboutBtn = document.getElementById("about");
  aboutBtn.addEventListener("click", function() {
    window.location.href = "/about";
  });

// define a function to redirect to dashboard page
var aboutBtn = document.getElementById("Dashboard");
  aboutBtn.addEventListener("click", function() {
    window.location.href = "/dashboard";
  });

// define a function to redirect to crime reports page
var reportsBtn = document.getElementById("reports");
reportsBtn.addEventListener("click", function() {
    window.location.href = "/dash";
  });

  
var denverbtn = document.getElementById("denver");
denverbtn.addEventListener("click", function() {
    window.location.href = "/denver";
  });

var contactbtn = document.getElementById("contact");
contactbtn.addEventListener("click", function() {
  window.location.href = "/contacts";
});



// define a function to logout from dashboard
var logout_bool = false;
logout_bool = document.getElementById("logout")
function logout() {
  if (logout_bool){
    window.location.href = "/logout";
  }
}

var report_boolean = false
report_boolean = document.getElementById("report")

function reportCrime(){
  if(report_boolean){
    // open a google form containing important fields
    window.open('https://forms.gle/Zip3XEp2X9ciMb9m6')
  }
}
var contact_bool = false
contact_bool = document.getElementById("contact")
function contact(){
  if(contact_bool){
    window.location.href("/contacts")
  }
}

// ---------- CHARTS ------------


// Bar chart
var barChartOptions = {
    series: [{
    data: [10,8,6,4,2]
  }],
    chart: {
    type: 'bar',
    height: 350,
    toolbar: {
        show:false
    },
  },
  colors : [
    "#246dec",
    "#cc3c43",
    "#367952",
    "#f5b74f",
    "#4f35a1"
  ],
  plotOptions: {
    bar: {
      distributed: true,  
      borderRadius: 4,
      horizontal: false,
      columnWidth : '40%',
    }
  },
  dataLabels: {
    enabled: false
  },
  xaxis: {
    categories: ["Theft", "Assault", "Violence", "Vandalism", "Harassment"
    ],
  },
  yaxis : {
    title: "Count"
  }
  };

var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
barChart.render();


// ----- Area Chart ----
var areaChartOptions = {
  series: [{
  name: 'Crime Clearence Rate',
  type: 'area',
  data: [44, 55, 31, 47, 31, 43, 26, 41, 31, 47, 33]
}, {
  name: 'Repeat Offender Rate',
  type: 'line',
  data: [55, 69, 45, 61, 43, 54, 37, 52, 44, 61, 43]
}],
  chart: {
  height: 350,
  type: 'line',
},
stroke: {
  curve: 'smooth'
},
fill: {
  type:'solid',
  opacity: [0.35, 1],
},
labels: ['2005', '2006','2007','2008','2009','2010','2011','2012','2013 ','2014','2015'],
markers: {
  size: 0
},
yaxis: [
  {
    title: {
      text: 'Crime Clearence Rate',
    },
  },
  {
    opposite: true,
    title: {
      text: 'Repeat Offender Rate',
    },
  },
],
tooltip: {
  shared: true,
  intersect: false,
  y: {
    formatter: function (y) {
      if(typeof y !== "undefined") {
        return  y.toFixed(0) + " points";
      }
      return y;
    }
  }
}
};

var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
areaChart.render();