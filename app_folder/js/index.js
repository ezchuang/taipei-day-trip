// 全域變數宣告
let nextPage = 0
let keyword = null


// Load More
let observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting){
            generateAttractionsController();
        }
    })
})
// 固定的 Observer Target (應該不需要特別寫成 const)
let observerTarget = document.querySelector(".footer")


// 網頁轉跳 for div
function linkToUrl(url){
    window.location.href = url;
}


// get attrctions api url
function getAttractionsUrl(page=null, keyword=null){
    let res = `/api/attractions?page=${page}`
    if (! keyword){
        return res
    }
    return res + `&keyword=${keyword}`
}


// Load more 監聽
function createObserver(target){
    observer.observe(target)
}
function removeObserver(target){
    observer.unobserve(target)
}


// 錯誤發生時，顯示錯誤訊息
function generateErrorMsg(msg){
    let attractionsGroup = document.querySelector("#attractionsGroup");
    let errorMsg = document.createElement("div");
    attractionsGroup.appendChild(errorMsg)
    errorMsg.classList.add("errorMsg")
    msgTextNode = document.createTextNode(msg)
    errorMsg.append(msgTextNode)
}


// 頁面更換 fetch(search) target 時，刷新(重建)主要區塊
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


// MrtList 左鍵行為
function arrowLeft(){
    let mrtContainer =  document.querySelector("#container")
    let containerWidth = mrtContainer.offsetWidth;
    mrtContainer.scrollBy({
        left: -containerWidth + 40,
        behavior: "smooth",
    });
}


// MrtList 右鍵行為
function arrowRight(){
    let mrtContainer =  document.querySelector("#container")
    let containerWidth = mrtContainer.offsetWidth;
    mrtContainer.scrollBy({
        left: containerWidth - 40,
        behavior: "smooth",
    });
}


// 搜尋關鍵字
function setKeyword(){
    // reset parameters
    nextPage = 0
    keyword = document.querySelector("#searchInput").value

    // page implement
    freshPage()
    generateAttractionsController()
}


// 從 MrtList 搜尋關鍵字
function setKeywordMrt(mrtName){
    document.querySelector("#searchInput").value = mrtName.textContent
    setKeyword()
} 


// 生成 MRT List
async function generateMrts(){
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
        listItem.classList.add("pointer")
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


// generateAttractions 實作的(加入元素)的部分
function generateAttractions(attractionsGroup, attractionsData, order){
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
    attraction.classList.add("pointer");
    attraction.setAttribute("onClick", `linkToUrl('/attraction/${attractionsData[order].id}')`)
    imgAndName.classList.add("imgAndName");
    mask.classList.add("mask");
    attractionImg.classList.add("attractionImg");
    attractionImg.setAttribute("alt", attractionsData[order].name);
    attractionImg.setAttribute("src", attractionsData[order].images[0]);
    detailNameFrame.classList.add("detailNameFrame");
    detailName.classList.add("detailName");
    rectangle.classList.add("rectangle");
    infos.classList.add("infos");
    attractionName.classList.add("attractionName");
    attractionName.classList.add("whiteText");
    attractionName.classList.add("bold");
    let textAttractionName = document.createTextNode(attractionsData[order].name);
    attractionName.appendChild(textAttractionName);
    detailMrtCatFrame.classList.add("detailMrtCatFrame");
    detailMrtCat.classList.add("detailMrtCat");
    detailMrt.classList.add("detailMrt");
    detailMrt.classList.add("bold");
    detailMrt.classList.add("grayColor-50");
    let textAttractionMrt = document.createTextNode(attractionsData[order].mrt);
    detailMrt.appendChild(textAttractionMrt);
    detailCat.classList.add("detailCat");
    detailCat.classList.add("bold");
    detailCat.classList.add("grayColor-50");
    let textAttractionCat = document.createTextNode(attractionsData[order].category);
    detailCat.appendChild(textAttractionCat);
}


// 生成 Attractions List
async function generateAttractionsController(){
    // observe 移除(視條件於本函式尾部重啟)
    removeObserver(observerTarget)

    let tempAttractionsDatas = await fetch(getAttractionsUrl(nextPage, keyword))
    let attractionsDataObj = await tempAttractionsDatas.json()
    console.log(attractionsDataObj)

    // 異常驗證
    if (Object.hasOwn(attractionsDataObj, "error")){
        generateErrorMsg(attractionsDataObj.message)
        return
    }

    let attractionsData = attractionsDataObj.data
    nextPage = attractionsDataObj.nextPage
    let attractionsGroup = document.querySelector("#attractionsGroup");

    for (let i=0; i < attractionsData.length; i++){
        generateAttractions(attractionsGroup, attractionsData, i)
    }

    // 終止驗證，不讓 observerTarget 重新被 observe
    if (nextPage == null || attractionsData.length < 12){
        return
    }

    // observe 復歸
    createObserver(observerTarget)
}


// 網頁載入
document.addEventListener("DOMContentLoaded", function(){
    // 處理 mrt list
    generateMrts();

    // 處理 attraction list
    generateAttractionsController().then(()=>{
        // 建立 observe 
        createObserver(observerTarget)
    });
})

document.querySelector("#searchBtn").addEventListener("click", setKeyword)
document.querySelector("#arrowLeft").addEventListener("click", arrowLeft)
document.querySelector("#arrowRight").addEventListener("click", arrowRight)