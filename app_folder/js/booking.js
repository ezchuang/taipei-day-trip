function generateAttractionsBookingFrame(attractionFrame, data){
    let attractionInsertTarget = document.createElement("div")
    attractionFrame.appendChild(attractionInsertTarget)

    // 圖片
    let attractionImg = document.createElement("div")
    let attractionImgInsertTarget = document.createElement("img")
    attractionInsertTarget.appendChild(attractionImg)
    attractionImg.appendChild(attractionImgInsertTarget)

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
    // price
    let attractionPrice = document.createElement("div")
    let attractionPriceLabel = document.createElement("div")
    let attractionPriceCnt = document.createElement("div")
    attractionInfo.appendChild(attractionPrice)
    attractionPrice.appendChild(attractionPriceLabel)
    attractionPrice.appendChild(attractionPriceCnt)
    // location
    let attractionLoc = document.createElement("div")
    let attractionLocLabel = document.createElement("div")
    let attractionLocCnt = document.createElement("div")
    attractionInfo.appendChild(attractionLoc)
    attractionLoc.appendChild(attractionLocLabel)
    attractionLoc.appendChild(attractionLocCnt)

    // delete button
    let delImgFrame = document.createElement("div")
    let delImg = document.createElement("img")
    attractionInsertTarget.appendChild(delImgFrame)
    delImgFrame.appendChild(delImg)


    // 賦予屬性
    attractionInsertTarget.classList.add("attractionInsertTarget")
        // attractionInsertTarget.setAttribute("id", `booking${data.attraction.id}`)
    // 圖片
    attractionImg.classList.add("attractionImg")
    attractionImgInsertTarget.classList.add("attractionImgInsertTarget")
    attractionImgInsertTarget.setAttribute("src", data.attraction.image)
    // info
    attractionInfo.classList.add("attractionInfo")
    // Name
    attractionName.classList.add("attractionName")
    attractionName.classList.add("bold")
    attractionName.classList.add("cyanText")
        // attractionNameLabel.classList.add("attractionNameLabel")
        // attractionNameLabel.textContent = ""
    attractionNameCnt.classList.add("attractionNameCnt")
    attractionNameCnt.textContent = `台北一日遊： ${data.attraction.name}`
    // date
    attractionDate.classList.add("attractionDate")
    attractionDateLabel.classList.add("attractionDateLabel")
    attractionDateLabel.classList.add("bold")
    attractionDateLabel.textContent = "日期："
    attractionDateCnt.classList.add("attractionDateCnt")
    attractionDateCnt.classList.add("medium")
    attractionDateCnt.textContent = data.date
    // time
    attractionTime.classList.add("attractionTime")
    attractionTimeLabel.classList.add("attractionTimeLabel")
    attractionTimeLabel.classList.add("bold")
    attractionTimeLabel.textContent = "時間："
    attractionTimeCnt.classList.add("attractionTimeCnt")
    attractionTimeCnt.classList.add("medium")
    if (data.time === "morning"){
        attractionTimeCnt.textContent = "上午 9 點到中午 12 點"
    }else if(data.time === "afternoon"){
        attractionTimeCnt.textContent = "中午 12 點到下午 4 點"
    }
    // price
    attractionPrice.classList.add("attractionPrice")
    attractionPriceLabel.classList.add("attractionPriceLabel")
    attractionPriceLabel.classList.add("bold")
    attractionPriceLabel.textContent = "費用："
    attractionPriceCnt.classList.add("attractionPriceCnt")
    attractionPriceCnt.classList.add("medium")
    attractionPriceCnt.textContent = `新台幣 ${data.price} 元`
    // location
    attractionLoc.classList.add("attractionLoc")
    attractionLocLabel.classList.add("attractionLocLabel")
    attractionLocLabel.classList.add("bold")
    attractionLocLabel.textContent = "地點："
    attractionLocCnt.classList.add("attractionLocCnt")
    attractionLocCnt.classList.add("medium")
    attractionLocCnt.textContent = data.attraction.address
    // delete button
    delImgFrame.classList.add("delImgFrame")
    delImg.classList.add("delImg")
    delImg.setAttribute("src", "/static/images/del.png")
    delImgFrame.addEventListener("click", () => {
        delBooking(attractionFrame, attractionInsertTarget, data.attraction.bookingId)
    })
}


// 刪除按鈕
async function delBooking(attractionFrame, delTarget, delId){
    let bodyFetchData = JSON.stringify({
        "id" : delId
    })
    let res = await fetchPackager({urlFetch:"/api/booking", methodFetch:"DELETE", bodyFetch:bodyFetchData})
    res = await res.json()

    if (res["error"]){
        let bookingErrMsg = document.createElement("div")
        delTarget.appendChild(bookingErrMsg)
        bookingErrMsg.setAttribute("bookingErrMsg")
        bookingErrMsg.textContent = res["message"]
        return 
    }
    attractionFrame.removeChild(delTarget)
    calculatePrice()
    checkExistence()
}


// 刷新價格
function calculatePrice(){
    let checkPriceCnt = document.querySelector(".checkPriceCnt")
    let totalPrice = 0
    let priceArr = document.querySelectorAll(".attractionPriceCnt")
    for (let i=0; i<priceArr.length; i++){
        totalPrice += Number(priceArr[i].textContent.split(" ")[1])
    }
    checkPriceCnt.textContent = `新台幣 ${totalPrice} 元`
}


// 有行程時注入
async function insertData(){
    let rawData = await fetchPackager({urlFetch:"/api/booking", methodFetch:"GET"})
    rawData = await rawData.json()

    let titleName = document.querySelector(".titleName")

    let name = document.cookie
        .split("; ")
        .find((row) => row.startsWith("name="))
        ?.split("=")[1]

    titleName.textContent = `您好，${name}，待預訂行程如下：`

    // 沒有預定行程
    if (! rawData.data[0].date){
        let innerFrame = document.querySelector(".innerFrame")
        let emptyMsg = document.querySelector(".emptyMsg")
        innerFrame.style.display = "none"
        emptyMsg.style.display = "flex"
        return
    }

    let dataList = rawData.data
    // 有預定行程
    let attractionFrame = document.querySelector(".attractionFrame")
    for (let i=0; i<dataList.length; i++){
        generateAttractionsBookingFrame(attractionFrame, dataList[i])
    }
}


// 檢驗是否尚有行程未下定
function checkExistence(){
    let attractionFrame = document.querySelector(".attractionFrame")

    if (attractionFrame.children.length > 0){
        return
    }
    let innerFrame = document.querySelector(".innerFrame")
    let emptyMsg = document.querySelector(".emptyMsg")
    innerFrame.style.display = "none"
    emptyMsg.style.display = "flex"
    return
}


// 監聽事件
document.addEventListener("DOMContentLoaded", async () => {
    if (! verified){
        url = "/"
        linkToUrl(url)
    }
    await insertData()
    calculatePrice()
})
document.querySelector("#signin").addEventListener("click", async () => {
    await sleep(500)
    url = "/"
    linkToUrl(url)
})
