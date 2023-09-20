// 宣告全域變數
let currentImgNum = null // 目前圖片編號
let imgAmount = null // 共幾張圖
let switchingFlag = false // 是否切換中 <- 為什麼加了這個就異常?
let imageArr = [] // image array 儲存image 網址


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


function changePlaceholderOfDate(){
    let placeholder = document.querySelector(".bookingDateInput")
    placeholder.setAttribute("placeholder", "yyyy/mm/dd")
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

    
    imageArr = data_target.images
    imgAmount = imageArr.length // 全域變數: 共幾張圖

    let imgInsertTarget = document.querySelector("#imgInsertTarget")
    imgInsertTarget.style.left = imgInsertTarget.offsetWidth
    if (imgAmount < 2){ // 只有一張圖
        currentImgNum = 0
        document.querySelector(".leftContainer").style.display = "none"
        document.querySelector(".rightContainer").style.display = "none"

        let imgDiv = document.createElement("div")
        let img = document.createElement("img")
        imgInsertTarget.appendChild(imgDiv)
        imgDiv.appendChild(img)
        imgDiv.classList.add("imgContainer")
        img.classList.add("imgTarget")
        
        img.setAttribute("id", `img0`)
        img.setAttribute("alt", `img0`)
        img.setAttribute("src", images[currentImgNum])
        return 
    }
    if (imgAmount < 1){ // 沒有圖
        let div = document.createElement("div")
        imgInsertTarget.appendChild(div)
        imgInsertTarget.textContent = "no image"
        div.setAttribute("class", "errorMsg")
        return
    }
        
    for (let i = 0; i < 3; i++){
        currentImgNum = 0

        let imgDiv = document.createElement("div")
        let img = document.createElement("img")
        imgInsertTarget.appendChild(imgDiv)
        imgDiv.appendChild(img)
        imgDiv.classList.add("imgContainer")
        img.classList.add("imgTarget")
        
        img.setAttribute("id", `img${i}`)
    }
    for (let i = 0; i < imgAmount; i++){
        // 插入小圓點
        let imgPositionCircleButton = document.querySelector("#imgPositionCircleButton")
        let imgButton = document.createElement("div")
        imgPositionCircleButton.appendChild(imgButton)
        imgButton.classList.add("imgButtonWhite")
        imgButton.setAttribute("id", `imgButton${String(i)}`)
    }
    for (let i = 0; i < 3; i++){
        // 注意!!!
        let img = document.querySelector(`#img${i}`)
        index = ((i -1 + imgAmount) % imgAmount)
        img.setAttribute("alt", `img${index}`)
        img.setAttribute("src", imageArr[index])
    }
    switchButton()
}


// 圖片移動動畫 與 圖片切換
function moveImg(next){
    let imgContainer = document.querySelector(`.imgContainer`)
    // let imgCurrent = document.querySelector(`#img${current}`)
    let translateValue = next * 100 - 100
    // transition: transform 1s ease-in-out;
    imgContainer.style.transform = translateX(`${translateValue}%`)
}


// 圖片位置校正
function switchImg(next){
    for (let i = 0; i < 3; i++){
        let imgCurrent = document.querySelector(`#img${i}`)
        imgCurrent.setAttribute("src", imageArr[((next + i - 1 + imgAmount) % imgAmount)])
        
    }
    let imgContainer = document.querySelector(`.imgContainer`)
    imgContainer.style.transition = "none"
    imgContainer.style.transform = translateX(`100%`)
    imgContainer.style.transition = "transform 1s ease-in-out;"
}


// MrtList 左鍵行為
function arrowLeft(){
    // [nextImgNum, currentImgNum, previousImgNum] = moveImg(nextImgNum, currentImgNum, previousImgNum, previousImgNum - 1);
    // [nextImgNum, currentImgNum, previousImgNum] = switchImg(nextImgNum, currentImgNum, previousImgNum, previousImgNum - 1);
    currentImgNum = currentImgNum - 1
    moveImg(-1)
    switchImg(currentImgNum)
    switchButton()
}
// MrtList 右鍵行為
function arrowRight(){
    // [previousImgNum, currentImgNum, nextImgNum] = moveImg(previousImgNum, currentImgNum, nextImgNum, nextImgNum + 1);
    // [previousImgNum, currentImgNum, nextImgNum] = switchImg(previousImgNum, currentImgNum, nextImgNum, nextImgNum + 1);
    currentImgNum = currentImgNum + 1
    moveImg(1)
    switchImg(currentImgNum)
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
    changePlaceholderOfDate()
})
document.querySelector("#arrowLeft").addEventListener("click", arrowLeft)
document.querySelector("#arrowRight").addEventListener("click", arrowRight)
document.querySelector(".bookingTimeFrame").addEventListener("click", showPrice)