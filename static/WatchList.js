 function setCookie(name, value, daysToLive) {
    // Encode value in order to escape semicolons, commas, and whitespace
    var cookie = name + "=" + encodeURIComponent(value);

    if(typeof daysToLive === "number") {
        /* Sets the max-age attribute so that the cookie expires
        after the specified number of days */
        cookie += "; max-age=" + (daysToLive*24*60*60);
        document.cookie = cookie;
    }
  }
  function addfunc1(){
    var b1 = document.getElementById("13");
    if(b1.style.display == "none"){
      b1.style.display = "block";
      var name= document.getElementById("sleList1").value;
      b1.innerHTML=name;
      document.getElementById("12").disabled = true;
      document.getElementById("11").disabled = false;
      document.getElementById("sleList1").hidden=false; // opt will appear
      setCookie("13",name,1);
    }
    else{
      b1.style.display="none";
    }
  }
  function remfunc1(){
    var b1 = document.getElementById("13");
    b1.style.display = "none";
    document.getElementById("12").disabled = false;
    document.getElementById("11").disabled = true;
    document.getElementById("sleList1").hidden=false; // opt will appear
    document.cookie = "13=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
  }

  function addfunc2(){
    var b1 = document.getElementById("23");
    if(b1.style.display == "none"){
      b1.style.display = "block";
      var name= document.getElementById("sleList2").value;
      b1.innerHTML=name;
      document.getElementById("22").disabled = true;
      document.getElementById("21").disabled = false;
      setCookie("23",name,1);
    }
    else{
      b1.style.display="none";
    }
  }
  function remfunc2(){
    var b1 = document.getElementById("23");
    b1.style.display = "none";
    document.getElementById("22").disabled = false;
    document.getElementById("21").disabled = true;
    document.getElementById("sleList2").hidden=false; // opt will appear
    document.cookie = "23=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
  }

  function addfunc3(){
    var b1 = document.getElementById("33");
    if(b1.style.display == "none"){
      b1.style.display = "block";
      var name= document.getElementById("sleList3").value;
      b1.innerHTML=name;
      document.getElementById("32").disabled = true;
      document.getElementById("31").disabled = false;
      setCookie("33",name,1);
    }
    else{
      b1.style.display="none";
    }
  }
  function remfunc3(){
    var b1 = document.getElementById("33");
    b1.style.display = "none";
    document.getElementById("32").disabled = false;
    document.getElementById("31").disabled = true;
    document.getElementById("sleList3").hidden=false; // opt will appear
    document.cookie = "33=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
  }

  function addfunc4(){
    var b1 = document.getElementById("43");
    if(b1.style.display == "none"){
      b1.style.display = "block";
      var name= document.getElementById("sleList4").value;
      b1.innerHTML=name;
      document.getElementById("42").disabled = true;
      document.getElementById("41").disabled = false;
      setCookie("43",name,1);
    }
    else{
      b1.style.display="none";
    }
  }
  function remfunc4(){
    var b1 = document.getElementById("43");
    b1.style.display = "none";
    document.getElementById("42").disabled = false;
    document.getElementById("41").disabled = true;
    document.getElementById("sleList4").hidden=false; // opt will appear
    document.cookie = "43=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
  }

  function addfunc5(){
    var b1 = document.getElementById("53");
    if(b1.style.display == "none"){
      b1.style.display = "block";
      var name= document.getElementById("sleList5").value;
      b1.innerHTML=name;
      document.getElementById("52").disabled = true;
      document.getElementById("51").disabled = false;
      setCookie("53",name,1);
    }
    else{
      b1.style.display="none";
    }
  }
  function remfunc5(){
    var b1 = document.getElementById("53");
    b1.style.display = "none";
    document.getElementById("52").disabled = false;
    document.getElementById("51").disabled = true;
    document.getElementById("sleList5").hidden=false; // opt will appear
    document.cookie = "53=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
  }

  function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");
    
    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
      var cookiePair = cookieArr[i].split("=");

      /* Removing whitespace at the beginning of the cookie name
      and compare it with the given string */
      if(name == cookiePair[0].trim()) {
          // Decode the cookie value and return
          return decodeURIComponent(cookiePair[1]);
      }
    }
  }

  // A custom function to check cookies
  function checkCookie() {
    // Get cookie using our custom function
    arr=["13","23","33","43","53"];
    
    for (let i = 0; i < 5; i++) {
      var firstName = getCookie(arr[i]);
      var addBt = (parseInt(arr[i]) - 1).toString();
      
      if(firstName != null) {
        var b1 = document.getElementById(arr[i]);
        var remBt = (parseInt(arr[i]) - 1).toString();
        var addBt = (parseInt(arr[i]) - 1).toString();
        var opt = "sleList" + (i+1).toString();
        b1.style.display = "block";
        b1.innerHTML=firstName;
        document.getElementById(remBt).disabled = false;
        document.getElementById(addBt).disabled = true;
        document.getElementById(opt).hidden=true;
      }
    }
  }
  
  // Check the cookie on page load
  window.onload=checkCookie();  