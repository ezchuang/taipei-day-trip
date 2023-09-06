let nextPage = 0
let keyword = null

// 網頁轉跳 for div
function linkToUrl(url){
    window.location.href = url;
}

// get attrctions api url
function getAttractionsUrl(page=0, keyword=null){
    // let res = `/api/attractions?page=${page}`
    let res = `/api/attractions?page=${page}`
    if (! keyword){
        return res
    }
    return res + `&keyword=${keyword}`
}

function generateErrorMsg(msg){
    let attractionsGroup = document.querySelector("#attractionsGroup");
    let errorMsg = document.createElement("div");
    attractionsGroup.appendChild(errorMsg)
    errorMsg.classList.add("errorMsg")
    msgTextNode = document.createTextNode(msg)
    errorMsg.append(msgTextNode)
}

function freshPage(){
    // drop
    let parent = document.querySelector("#attractionsFrame")
    let child = document.querySelector("#attractionsGroup")
    parent.removeChild(child)

    // generate Frame
    child = document.createElement("div");
    parent.appendChild(child)
    child.setAttribute("id", "attractionsGroup")
}

function arrowLeft(){
    let mrtContainer =  document.querySelector("#container")
    let containerWidth = mrtContainer.offsetWidth;
    mrtContainer.scrollBy({
        left: -containerWidth + 40,
        behavior: "smooth",
    });
}

function arrowRight(){
    let mrtContainer =  document.querySelector("#container")
    let containerWidth = mrtContainer.offsetWidth;
    mrtContainer.scrollBy({
        left: containerWidth - 40,
        behavior: "smooth",
    });
}

function setKeyword(){
    // reset parameters
    nextPage = 0
    keyword = document.querySelector("#searchInput").value
    // document.querySelector("#searchInput").value = keyword

    // page implement
    freshPage()
    generateAttractions()
}

function setKeywordMrt(mrtName){
    document.querySelector("#searchInput").value = mrtName.textContent
    setKeyword()
} 

// 生成 MRT List
async function generateMrts(){
    // let tempMrtData = await fetch("/api/mrts")
    let tempMrtData = await fetch("/api/mrts")
    let mrtDataObj = await tempMrtData.json()
    let mrtData = mrtDataObj.data

    let listItemContainer = document.querySelector("#listItemContainer");

    for (let i=0; i < mrtData.length; i++){
        // 生成框架
        let listItem = document.createElement("div");
        listItemContainer.appendChild(listItem)

        // 加入元素
        listItem.classList.add("listItem")
        listItem.classList.add("bold")
        let mrtName
        if (! mrtData[i]){
            continue;
        }else{
            mrtName = document.createTextNode(mrtData[i]);
        };
        listItem.appendChild(mrtName)

        // 動態生成
        listItem.setAttribute("onClick", `setKeywordMrt(this)`)
    }
}


// 生成 Attractions List
async function generateAttractions(){
    let tempAttractionsDatas = await fetch(getAttractionsUrl(nextPage, keyword))
    let attractionsDataObj = await tempAttractionsDatas.json()
    // 終止驗證
    if (Object.hasOwn(attractionsDataObj, "error")){
        if (attractionsDataObj["error"] & nextPage == 0){
            document.removeEventListener("scrollend", generateAttractions);
            generateErrorMsg(attractionsDataObj.message)
            return
        }
    }

    let attractionsData = attractionsDataObj.data
    nextPage = attractionsDataObj.nextPage

    let attractionsGroup = document.querySelector("#attractionsGroup");
    if (attractionsData.length < 12){
        document.removeEventListener("scrollend", generateAttractions);
    }
    for (let i=0; i < attractionsData.length; i++){
        // 生成框架
        let attraction = document.createElement("div");
        attractionsGroup.appendChild(attraction)

        let imgAndName = document.createElement("div");
        attraction.appendChild(imgAndName)

        let mask = document.createElement("div");
        let attractionImg = document.createElement("img");
        let detailNameFrame = document.createElement("div");
        imgAndName.appendChild(mask);
        imgAndName.appendChild(attractionImg);
        imgAndName.appendChild(detailNameFrame);

        let detailName = document.createElement("div");
        detailNameFrame.appendChild(detailName);

        let rectangle = document.createElement("div");
        let infos = document.createElement("div");
        detailName.appendChild(rectangle);
        detailName.appendChild(infos);

        let attractionName = document.createElement("div");
        infos.appendChild(attractionName);

        let detailMrtCatFrame = document.createElement("div");
        attraction.appendChild(detailMrtCatFrame);

        let detailMrtCat = document.createElement("div");
        detailMrtCatFrame.appendChild(detailMrtCat);

        let detailMrt = document.createElement("div");
        let detailCat = document.createElement("div");
        detailMrtCat.appendChild(detailMrt);
        detailMrtCat.appendChild(detailCat);

        // 加入元素
        attraction.classList.add("attraction");
        attraction.setAttribute("onClick", `linkToUrl('/attraction/${attractionsData[i].id}')`)
        imgAndName.classList.add("imgAndName");
        mask.classList.add("mask");
        attractionImg.classList.add("attractionImg");
        attractionImg.setAttribute("alt", attractionsData[i].name);
        attractionImg.setAttribute("src", attractionsData[i].images[0]);
        detailNameFrame.classList.add("detailNameFrame");
        detailName.classList.add("detailName");
        rectangle.classList.add("rectangle");
        infos.classList.add("infos");
        attractionName.classList.add("attractionName");
        attractionName.classList.add("whiteText");
        attractionName.classList.add("bold");
        let textAttractionName = document.createTextNode(attractionsData[i].name);
        attractionName.appendChild(textAttractionName);
        detailMrtCatFrame.classList.add("detailMrtCatFrame");
        detailMrtCat.classList.add("detailMrtCat");
        detailMrt.classList.add("detailMrt");
        detailMrt.classList.add("bold");
        detailMrt.classList.add("grayColor-50");
        let textAttractionMrt = document.createTextNode(attractionsData[i].mrt);
        detailMrt.appendChild(textAttractionMrt);
        detailCat.classList.add("detailCat");
        detailCat.classList.add("bold");
        detailCat.classList.add("grayColor-50");
        let textAttractionCat = document.createTextNode(attractionsData[i].category);
        detailCat.appendChild(textAttractionCat);
    }
}

// 網頁載入
document.addEventListener("DOMContentLoaded", async function(){
    // 處理 mrt list
    generateMrts();

    // 處理 attraction list
    generateAttractions();
})

document.addEventListener("scrollend", generateAttractions)

document.querySelector("#searchBtn").addEventListener("click", setKeyword)
document.querySelector("#arrowLeft").addEventListener("click", arrowLeft)
document.querySelector("#arrowRight").addEventListener("click", arrowRight)