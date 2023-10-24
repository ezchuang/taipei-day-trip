let urlParams  = new URLSearchParams(window.location.search);
let orderId = urlParams.get("number")
// 宣告全域變數
let dataList
let totalPrice = 0

function generateAttractionsOrdersFrame(attractionFrame, data){
    console.log(data)
    let attractionInsertTarget = document.createElement("div")
    attractionFrame.appendChild(attractionInsertTarget)

    // 圖片
    // let attractionImg = document.createElement("div")
    // let attractionImgInsertTarget = document.createElement("img")
    // attractionInsertTarget.appendChild(attractionImg)
    // attractionImg.appendChild(attractionImgInsertTarget)

    // info
    let attractionInfo = document.createElement("div")
    attractionInsertTarget.appendChild(attractionInfo)
    // Name
    let attractionName = document.createElement("div")
        // let attractionNameLabel = document.createElement("div")
    let attractionNameCnt = document.createElement("div")
    attractionInfo.appendChild(attractionName)
        // attractionName.appendChild(attractionNameLabel)
    attractionName.appendChild(attractionNameCnt)
    // date
    let attractionDate = document.createElement("div")
    let attractionDateLabel = document.createElement("div")
    let attractionDateCnt = document.createElement("div")
    attractionInfo.appendChild(attractionDate)
    attractionDate.appendChild(attractionDateLabel)
    attractionDate.appendChild(attractionDateCnt)
    // time
    let attractionTime = document.createElement("div")
    let attractionTimeLabel = document.createElement("div")
    let attractionTimeCnt = document.createElement("div")
    attractionInfo.appendChild(attractionTime)
    attractionTime.appendChild(attractionTimeLabel)
    attractionTime.appendChild(attractionTimeCnt)
    // location
    let attractionLoc = document.createElement("div")
    let attractionLocLabel = document.createElement("div")
    let attractionLocCnt = document.createElement("div")
    attractionInfo.appendChild(attractionLoc)
    attractionLoc.appendChild(attractionLocLabel)
    attractionLoc.appendChild(attractionLocCnt)

    // 賦予屬性
    attractionInsertTarget.classList.add("attractionInsertTarget")
        // attractionInsertTarget.setAttribute("id", `Orders${data.attraction.id}`)
    // 圖片
    // attractionImg.classList.add("attractionImg")
    // attractionImgInsertTarget.classList.add("attractionImgInsertTarget")
    // attractionImgInsertTarget.setAttribute("src", data.attraction.image)
    // info
    attractionInfo.classList.add("attractionInfo")
    // Name
    attractionName.classList.add("attractionName")
    attractionName.classList.add("bold")
    attractionName.classList.add("cyanText")
    attractionName.classList.add("pointer")
    attractionName.setAttribute("onClick", `linkToUrl('/thankyou?number=${data.number}')`)
    attractionNameCnt.classList.add("attractionNameCnt")
    attractionNameCnt.textContent = `Order ID： ${data.number}`
    // date
    attractionDate.classList.add("attractionDate")
    attractionDateLabel.classList.add("attractionDateLabel")
    attractionDateLabel.classList.add("bold")
    attractionDateLabel.textContent = "訂單價格："
    attractionDateCnt.classList.add("attractionDateCnt")
    attractionDateCnt.classList.add("medium")
    attractionDateCnt.textContent = data.price
    // time
    attractionTime.classList.add("attractionTime")
    attractionTimeLabel.classList.add("attractionTimeLabel")
    attractionTimeLabel.classList.add("bold")
    attractionTimeLabel.textContent = "訂單姓名："
    attractionTimeCnt.classList.add("attractionTimeCnt")
    attractionTimeCnt.classList.add("medium")
    attractionTimeCnt.textContent = data.name

    // if (data.time === "morning"){
    //     attractionTimeCnt.textContent = "上午 9 點到中午 12 點"
    // }else if(data.time === "afternoon"){
    //     attractionTimeCnt.textContent = "中午 12 點到下午 4 點"
    // }
    // location
    attractionLoc.classList.add("attractionLoc")
    attractionLocLabel.classList.add("attractionLocLabel")
    attractionLocLabel.classList.add("bold")
    attractionLocLabel.textContent = "訂單狀態："
    attractionLocCnt.classList.add("attractionLocCnt")
    attractionLocCnt.classList.add("medium")
    // attractionLocCnt.textContent = data.status
    if (data.status === 1){
        attractionLocCnt.textContent = "已完成付款"
    }else if(data.status === 0){
        attractionLocCnt.textContent = "尚未完成付款"
    }
}


// 刷新價格
// function calculatePrice(){
//     let checkPriceCnt = document.querySelector(".checkPriceCnt")
//     checkPriceCnt.textContent = `新台幣 ${totalPrice} 元`
// }


// 訂單使用者資料顯示
// function generateAttractionsOrdersUserData(rawData){
//     let userNameCnt = document.querySelector(".userNameCnt")
//     let userEmailCnt = document.querySelector(".userEmailCnt")
//     let userNumberCnt = document.querySelector(".userNumberCnt")
//     userNameCnt.textContent = rawData.data.contact.name
//     userEmailCnt.textContent = rawData.data.contact.email
//     userNumberCnt.textContent = rawData.data.contact.phone
// }


// 有行程時注入
async function insertData(){
    let rawData = await fetchPackager({urlFetch:`/api/orders`, methodFetch:"GET"})
    rawData = await rawData.json()

    let titleName = document.querySelector(".titleName")
    // let titleOrderId = document.querySelector(".titleOrderId")

    let name = document.cookie
        .split("; ")
        .find((row) => row.startsWith("name="))
        ?.split("=")[1]

    titleName.textContent = `您好，${name} 訂單如下：`
    // titleOrderId.textContent = `訂單編號： ${orderId}`

    // 沒有行程
    if (! rawData.data){
        let innerFrame = document.querySelector(".innerFrame")
        let emptyMsg = document.querySelector(".emptyMsg")
        innerFrame.style.display = "none"
        emptyMsg.style.display = "flex"
        return
    }

    dataList = rawData.data
    // 有行程
    let attractionFrame = document.querySelector(".attractionFrame")
    for (let i=0; i<dataList.length; i++){
        generateAttractionsOrdersFrame(attractionFrame, dataList[i])
    }
    // generateAttractionsOrdersUserData(rawData)
}


// 監聽事件
document.addEventListener("DOMContentLoaded", async () => {
    if (! verified){
        url = "/"
        linkToUrl(url)
    }
    await insertData()
    // calculatePrice()
})
// 登出
document.querySelector("#signin").addEventListener("click", async () => {
    await sleep(500)
    url = "/"
    linkToUrl(url)
})