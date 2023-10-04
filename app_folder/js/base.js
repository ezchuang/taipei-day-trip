// 宣告全域變數
let verified = true

// 網頁轉跳 for div
function linkToUrl(url){
    window.location.href = url;
}


// 暫停
function sleep(time){
    return new Promise(resolve => setTimeout(resolve, time))
}


// del cookie
function delCookie(key) {
    var date = new Date();
    date.setTime(date.getTime() - 1000);
    document.cookie = `${key}='';expires=${date.toGMTString()}`;
}


// 按鈕修改
function signinJudge(success){
    let inpPageBtn = document.querySelector("#signin")
    if (! success){
        verified = false
        inpPageBtn.textContent = `登入/註冊`
        inpPageBtn.removeEventListener("click", logout)
        inpPageBtn.addEventListener("click", createSignin)
        return
    }
    verified = true
    inpPageBtn.textContent = `登出系統`
    inpPageBtn.removeEventListener("click", createSignin)
    inpPageBtn.addEventListener("click", logout)
}


// show error msg
function errMsg(msg){
    let errMsgFrame = document.querySelector(".errMsgFrame")
    errMsgFrame.style.display = "flex"
    errMsgFrame.textContent = msg
}


// create signin page
function createSignin(){
    // 建立結構
    let body = document.querySelector("body")
    let formOuterFrame = document.createElement("div")
    body.appendChild(formOuterFrame)

    
    let relativeFrame = document.createElement("div")
    let formMask = document.createElement("div")
    let formStyle = document.createElement("div")
    let formBanner = document.createElement("div")
    let formMiddleFrame = document.createElement("div")
    formOuterFrame.appendChild(relativeFrame)
    relativeFrame.appendChild(formMask)
    relativeFrame.appendChild(formStyle)
    formStyle.appendChild(formBanner)
    formStyle.appendChild(formMiddleFrame)
    
    let formTitle = document.createElement("div")
    let formInnerFrame = document.createElement("form")
    let nameIpt = document.createElement("input")
    let emailIpt = document.createElement("input")
    let pwIpt = document.createElement("input")
    let signinBtn = document.createElement("button")
    let errMsgFrame = document.createElement("div")
    let switchBtnFrame = document.createElement("div")
    formMiddleFrame.appendChild(formTitle)
    formMiddleFrame.appendChild(formInnerFrame)
    formInnerFrame.appendChild(nameIpt)
    formInnerFrame.appendChild(emailIpt)
    formInnerFrame.appendChild(pwIpt)
    formInnerFrame.appendChild(signinBtn)
    formInnerFrame.appendChild(errMsgFrame)
    formInnerFrame.appendChild(switchBtnFrame)

    let switchBtnText = document.createElement("div")
    let signinPageSwitchBtn = document.createElement("div")
    switchBtnFrame.appendChild(switchBtnText)
    switchBtnFrame.appendChild(signinPageSwitchBtn)

    // 插入 class
    formOuterFrame.classList.add("formOuterFrame")
    relativeFrame.classList.add("relativeFrame")
    formMask.classList.add("formMask")
    formStyle.classList.add("formStyle")
    formBanner.classList.add("formBanner")

    formMiddleFrame.classList.add("formMiddleFrame")
    formTitle.classList.add("formTitle")
    formTitle.classList.add("h3")
    formTitle.classList.add("bold")
    formInnerFrame.classList.add("formInnerFrame")
    nameIpt.classList.add("nameIpt")
    nameIpt.classList.add("content")
    nameIpt.classList.add("medium")
    emailIpt.classList.add("emailIpt")
    emailIpt.classList.add("content")
    emailIpt.classList.add("medium")
    pwIpt.classList.add("pwIpt")
    pwIpt.classList.add("content")
    pwIpt.classList.add("medium")
    signinBtn.classList.add("signinBtn")
    signinBtn.classList.add("whiteText")
    signinBtn.classList.add("button")
    signinBtn.classList.add("regular")
    signinBtn.classList.add("pointer")
    errMsgFrame.classList.add("errMsgFrame")
    switchBtnFrame.classList.add("switchBtnFrame")
    switchBtnText.classList.add("switchBtnText")
    signinPageSwitchBtn.classList.add("signinPageSwitchBtn")
    signinPageSwitchBtn.classList.add("pointer")


    // 插入內容、id
    let titleText = document.createTextNode("登入會員帳號")
    formTitle.appendChild(titleText)
    formInnerFrame.setAttribute("onSubmit", "return false")
    nameIpt.setAttribute("type", "text")
    nameIpt.setAttribute("name", "nameIpt")
    nameIpt.setAttribute("id", "nameIpt")
    nameIpt.setAttribute("placeholder", "輸入姓名")
    nameIpt.style.display = "none"
    emailIpt.setAttribute("type", "email")
    emailIpt.setAttribute("name", "emailIpt")
    emailIpt.setAttribute("id", "emailIpt")
    emailIpt.setAttribute("placeholder", "輸入電子信箱")
    pwIpt.setAttribute("type", "password")
    pwIpt.setAttribute("name", "pwIpt")
    pwIpt.setAttribute("id", "pwIpt")
    pwIpt.setAttribute("placeholder", "輸入密碼")
    let signinBtnText = document.createTextNode("登入帳戶")
    signinBtn.appendChild(signinBtnText)
    let switchBtnTextText = document.createTextNode("還沒有帳戶?")
    switchBtnText.appendChild(switchBtnTextText)
    let signinPageSwitchBtnText = document.createTextNode("點此註冊")
    signinPageSwitchBtn.appendChild(signinPageSwitchBtnText)

    // 加入 Event
    formMask.addEventListener("click", removeSigninupPage)
    signinBtn.addEventListener("click", signin)
    signinPageSwitchBtn.addEventListener("click", showSignup)
}


// hide signin/signup page
function removeSigninupPage(){
    let body = document.querySelector("body")
    let formOuterFrame = document.querySelector(".formOuterFrame")
    body.removeChild(formOuterFrame)
}


// show signup page
function showSignup(){
    let formTitle =  document.querySelector(".formTitle")
    formTitle.textContent = "註冊會員帳號"

    let nameIpt =  document.querySelector(".nameIpt")
    nameIpt.style.display = "block"

    let signinBtn =  document.querySelector(".signinBtn")
    signinBtn.textContent = "註冊新帳戶"
    signinBtn.removeEventListener("click", signin)
    signinBtn.addEventListener("click", signup)

    let errMsgFrame = document.querySelector(".errMsgFrame")
    errMsgFrame.style.display = "none"

    let switchBtnText =  document.querySelector(".switchBtnText")
    switchBtnText.textContent = "已經有帳戶了?"

    let signinPageSwitchBtn =  document.querySelector(".signinPageSwitchBtn")
    signinPageSwitchBtn.textContent = "點此登入"


    signinPageSwitchBtn.removeEventListener("click", showSignup)
    signinPageSwitchBtn.addEventListener("click", showSignin)
}


// show signin page
function showSignin(){
    let formTitle =  document.querySelector(".formTitle")
    formTitle.textContent = "登入會員帳號"

    let nameIpt =  document.querySelector(".nameIpt")
    nameIpt.style.display = "none"

    let signinBtn =  document.querySelector(".signinBtn")
    signinBtn.textContent = "登入帳戶"
    signinBtn.removeEventListener("click", signup)
    signinBtn.addEventListener("click", signin)

    let errMsgFrame = document.querySelector(".errMsgFrame")
    errMsgFrame.style.display = "none"

    let switchBtnText =  document.querySelector(".switchBtnText")
    switchBtnText.textContent = "還沒有帳戶?"

    let signinPageSwitchBtn =  document.querySelector(".signinPageSwitchBtn")
    signinPageSwitchBtn.textContent = "點此註冊"

    signinPageSwitchBtn.removeEventListener("click", showSignin)
    signinPageSwitchBtn.addEventListener("click", showSignup)
}


// logout
function logout(){
    localStorage.removeItem("token")
    signinJudge(false)
}


// 註冊
async function signup(){
    let formInnerFrame = document.querySelector(".formInnerFrame")
    let name = formInnerFrame.querySelector("#nameIpt").value
    let email = formInnerFrame.querySelector("#emailIpt").value
    let password = formInnerFrame.querySelector("#pwIpt").value
    if (! name){
        errMsg("請輸入使用者名稱")
        return
    }else if (! email){
        errMsg("請輸入 e-mail")
        return
    }else if (! password){
        errMsg("請輸入密碼")
        return
    }
    if (! email){
        errMsg("請輸入 e-mail")
        return
    }else if (! password){
        errMsg("請輸入密碼")
        return
    }
    let signupResult = await fetch("/api/user", {
        method : "POST",
        body : JSON.stringify({
            "name" : name,
            "email" : email,
            "password" : password,
        }),
        headers : {
            "Content-Type" : "application/json",
        }
    })
    signupResult = await signupResult.json()
    if (signupResult.hasOwnProperty("error")){
        errMsg(signupResult.message)
        return
    }
    removeSigninupPage()
}


// 登入頁面
async function signin(){
    let formInnerFrame = document.querySelector(".formInnerFrame")
    let email = formInnerFrame.querySelector("#emailIpt").value
    let password = formInnerFrame.querySelector("#pwIpt").value
    if (! email){
        errMsg("請輸入 e-mail")
        return
    }else if (! password){
        errMsg("請輸入密碼")
        return
    }
    let userData = await fetch("/api/user/auth", {
        method : "PUT",
        body : JSON.stringify({
            "email" : email,
            "password" : password,
        }),
        headers : {
            "Content-Type" : "application/json",
        }
    })
    userData = await userData.json()
    if (userData.hasOwnProperty("error")){
        errMsg(userData.message)
        localStorage.clear()
        return
    }else{
        errMsg("登入成功")
    }
    localStorage.setItem("token", userData.token)

    await sleep(1000)

    removeSigninupPage()
    signinJudge(true)
    verifyUser()
}


// 驗證登入狀態
async function verifyUser(){
    let tokenValue = localStorage.getItem("token")
    if (! tokenValue){
        signinJudge(false)
        return false
    }
    let userData = await fetch("/api/user/auth", {
        method : "GET",
        headers :{
            "Authorization" : `Bearer ${tokenValue}`,
        }
    })
    userData = await userData.json()
    if (! userData.data){
        signinJudge(false)
        return false
    }
    document.cookie = `name=${userData.data.name}; `
    signinJudge(true)
            
    return true
}


// fetch to url
function fetchPackager({
    urlFetch="/", 
    methodFetch="GET", 
    headersFetch={
        "Authorization":`Bearer ${localStorage.getItem("token")}`,
        "Content-Type":"application/json",
        }, 
    bodyFetch=null}){

    let res = fetch(urlFetch, {
        method : methodFetch,
        headers : headersFetch,
        body : bodyFetch
    })
    return res
}


// 監聽事件
document.addEventListener("DOMContentLoaded", async () => {
    await verifyUser()
})
document.querySelector("#bookingPageBtn").addEventListener("click", () => {
    if (! verified){
        createSignin()
    }else{
        url = "/booking"
        linkToUrl(url)
    }
})