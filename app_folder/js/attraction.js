// 宣告全域變數
let  = null // 上一個圖片編號
let currentImgNum = null // 目前圖片編號
let nextImgNum = null // 下一個圖片編號
let imgAmount = null // 共幾張圖


// 抓網址 ID
function getID(){
    let dynamicUrl = window.location.pathname.split('/')
    let currentId = dynamicUrl.pop()
    return currentId
}


// 暫停
function sleep(time){
    return new Promise(resolve => setTimeout(resolve, time))
}


// 小圓點校正
function switchButton(){
    let buttonArr = document.querySelectorAll(".imgButtonBlack")
    buttonArr.forEach((button) => {
        button.classList.remove("imgButtonBlack")
        button.classList.add("imgButtonWhite")
    })
    let currentButton = document.querySelector(`#imgButton${currentImgNum}`)
    currentButton.classList.remove("imgButtonWhite")
    currentButton.classList.add("imgButtonBlack")
}


// 插入 fetch 元素
async function insertElement(currentId){
    let data_raw = await fetch(`/api/attraction/${currentId}`)
    let data_json = await data_raw.json()
    let data_target = data_json.data

    let profileTitle = document.querySelector("#profileTitle")
    let textAttractionName = document.createTextNode(data_target.name)
    profileTitle.appendChild(textAttractionName)

    let profileDescription = document.querySelector("#profileDescription")
    let textAttractionMrtAndCat = document.createTextNode(data_target.category + " at " + data_target.mrt)
    profileDescription.appendChild(textAttractionMrtAndCat)

    let infosDescription = document.querySelector("#infosDescription")
    let textAttractionDescription = document.createTextNode(data_target.description)
    infosDescription.appendChild(textAttractionDescription)

    let infosAddress = document.querySelector("#infosAddress")
    let textAttractionAddress = document.createTextNode(data_target.address)
    infosAddress.appendChild(textAttractionAddress)

    let infosTraffic = document.querySelector("#infosTraffic")
    let textAttractionTraffic = document.createTextNode(data_target.transport)
    infosTraffic.appendChild(textAttractionTraffic)

    
    let images = data_target.images
    imgAmount = images.length // 全域變數: 共幾張圖
    let imgInsertTarget = document.querySelector("#imgInsertTarget")
    imgInsertTarget.style.left = imgInsertTarget.offsetWidth
    if (images.length < 2){ // 只有一張圖
        document.querySelector(".leftContainer").style.display = "none"
        document.querySelector(".rightContainer").style.display = "none"

        let img = document.createElement("img")
        imgInsertTarget.appendChild(img)
        img.classList.add("imgContainer")
        
        img.setAttribute("id", `img0`)
        img.setAttribute("alt", `img0`)
        img.setAttribute("src", images[0])
        return 
    }
    if (images.length < 1){ // 沒有圖
        let div = document.createElement("div")
        imgInsertTarget.appendChild(div)
        div.setAttribute("class", "errorMsg")
        return
    }
    
    for (let i = -2; i <= images.length + 1; i++){
        
        let img = document.createElement("img")
        imgInsertTarget.appendChild(img)
        img.classList.add("imgContainer")

        // 多在頭尾建立各 2 個 img
        if (i <= -1){
            img.setAttribute("id", `img${String(i)}`)
            img.setAttribute("alt", `img${String(i)}`)
            img.setAttribute("src", images[images.length + i])
        }else if (i >= images.length){
            img.setAttribute("id", `img${String(i)}`)
            img.setAttribute("alt", `img${String(i)}`)
            img.setAttribute("src", images[0])
        }else{
            img.setAttribute("id", `img${String(i)}`)
            img.setAttribute("alt", `img${String(i)}`)
            img.setAttribute("src", images[i])
        }
        if (i <= -1 || i >= images.length){
            continue
        }

        // 插入小圓點 
        let imgPositionCircleButton = document.querySelector("#imgPositionCircleButton")
        let imgButton = document.createElement("div")
        imgPositionCircleButton.appendChild(imgButton)
        imgButton.classList.add("imgButtonWhite")
        imgButton.setAttribute("id", `imgButton${String(i)}`)
    }

    img0 = document.querySelector(`#img${0}`)
    img0.style.width = `100%`
    img0.style.display = "block"

    // for (let i = -1; i < 2; i++){ // 3 個
    //     img = document.querySelector(`#img${i}`)
    //     img.style.width = `100%`
    //     img.style.display = "block"
    // }

    previousImgNum = -1
    currentImgNum = 0
    nextImgNum = 1
    switchButton()
}


// 圖片移動動畫 與 圖片切換
async function moveImg(disappear, current, next, expand){
    let container =  document.querySelector("#imgInsertTarget")
    let containerWidth = container.offsetWidth
    let spec = 40 // 縮小刻度


    // 測試
    let nextImg = document.querySelector(`#img${String(next)}`)
    
    
    let disappearImg = document.querySelector(`#img${String(disappear)}`)
    let expandImg = document.querySelector(`#img${String(expand)}`)
    
    let widthChanged = containerWidth/spec
    let disappearImgWidth = containerWidth
    let expandImgWidth = 0


    // 測試
    nextImg.style.width = `100%`
    nextImg.style.display = "block"
    expandImg.style.width = `100%`
    expandImg.style.display = "block"


    expandImg.style.width = `${expandImgWidth}px`
    expandImg.style.display = "block"

    for (let i = spec; i > 0; i--){
        disappearImgWidth -= widthChanged
        disappearImg.style.width = `${disappearImgWidth}px`

        expandImgWidth += widthChanged
        expandImg.style.width = `${expandImgWidth}px`

        await sleep(5)
    }
    disappearImg.style.display = "none"

    return [current, next, expand] // 進位
}


// 圖片位置校正
function switchImg(previous, current, next){
    let indexArr = [previous, current, next]
    if (0 <= indexArr[1] && indexArr[1] <= imgAmount - 1){
        [indexArr[0], indexArr[2]].forEach((index) => {
            img = document.querySelector(`#img${index}`)
            img.style.width = `0%`
            img.style.display = "none"
        })
        return indexArr
    }
    // 超界
    // 歸零
    indexArr.forEach((index) => {
        img = document.querySelector(`#img${index}`)
        img.style.width = `0%`
        img.style.display = "none"
    })

    // 轉址
    // console.log("超界處理前",indexArr)
    if (indexArr[1] < 0){ // 往左超界
        for (let i = 0; i < 3; i++){
            indexArr[i] = imgAmount - i
        }
    }else{ // 往右超界
        for (let i = 0; i < 3; i++){
            indexArr[i] = -1 + i
        }
    }
    // console.log("超界", indexArr)
    
    // 重新給予寬度
    [indexArr[1]].forEach((index) => {
        img = document.querySelector(`#img${index}`)
        img.style.width = `100%`
        img.style.display = "block"
    })

    return indexArr
}


// MrtList 左鍵行為
async function arrowLeft(){
    [nextImgNum, currentImgNum, previousImgNum] = await moveImg(nextImgNum, currentImgNum, previousImgNum, previousImgNum - 1);
    [nextImgNum, currentImgNum, previousImgNum] = switchImg(nextImgNum, currentImgNum, previousImgNum, previousImgNum - 1);
    switchButton()
}
// MrtList 右鍵行為
async function arrowRight(){
    [previousImgNum, currentImgNum, nextImgNum] = await moveImg(previousImgNum, currentImgNum, nextImgNum, nextImgNum + 1);
    [previousImgNum, currentImgNum, nextImgNum] = switchImg(previousImgNum, currentImgNum, nextImgNum, nextImgNum + 1);
    switchButton()
}


// 顯示費用，由於抓父層驅動，觸發條件較為寬鬆一點點
function showPrice(){
    let bookingPriceInput = document.querySelector(".bookingPriceInput")
    document.querySelectorAll(".bookingTimeInput").forEach((radio) => {
        if (radio.checked){
            bookingPriceInput.textContent = `新台幣 ${radio.value} 元`
        }
    })
}


// 監聽事件
document.addEventListener("DOMContentLoaded", () => {
    let currentId = getID()
    insertElement(currentId)
})
document.querySelector("#arrowLeft").addEventListener("click", arrowLeft)
document.querySelector("#arrowRight").addEventListener("click", arrowRight)
document.querySelector(".bookingTimeFrame").addEventListener("click", showPrice)