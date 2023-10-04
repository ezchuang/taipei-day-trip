TPDirect.setupSDK(137077, 'app_nPu2YoU0Fzzk8UnymXQDFgd2a8z0Q8K2Bhx5TiRq7vBDLQDPde9c6a2zJDCO', 'sandbox')


// user defined function for set order (async function)
async function setOrder(prime){
    // 資料處理
    let dataListOpt = []
    let priceVerify = totalPrice
    for (let i=0; i<dataList.length; i++){
        let tempObj = dataList[i]
        priceVerify -= tempObj.price
        delete tempObj.price
        if (priceVerify < 0){
            alert("不要亂搞")
            return
        }
        dataListOpt.push(tempObj)
    }

    // request 構成
    let bodyFetchData = JSON.stringify({
        "prime": prime,
        "order": {
            "price": totalPrice,
            "trip": dataListOpt,
            "contact": {
                "name": document.querySelector('[name="userName"]').value,
                "email": document.querySelector('[name="userEmail"]').value,
                "phone": document.querySelector('[name="userNumber"]').value,
          }
        }
    })

    let res = await fetchPackager({
        urlFetch: "/api/orders", 
        methodFetch: "POST", 
        bodyFetch: bodyFetchData
    }) // headersFetch = default
    res = await res.json()
    console.log(res)
    return res
}



// Display ccv field
TPDirect.card.setup({
    fields: {
        number: {
            element: '#card-number',
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            element: '#card-expiration-date',
            placeholder: 'MM / YY'
        },
        ccv: {
            element: '#card-ccv',
            placeholder: 'ccv'
        }
    },
    styles: {
        'input': {
            'color': 'gray',
            'font-family': 'Noto Sans TC, sans-serif',
            'font-size': '16px',
            'font-style': 'normal',
            'line-height': '13.3px',
            'font-weight': '500',
        },
        'input.ccv': {
        },
        'input.expiration-date': {
        },
        'input.card-number': {
        },
        ':focus': {
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
    },
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
})


// 輸入時檢查是否完成 & 輸入中排版
TPDirect.card.onUpdate(function (update) {
    let submitButton = document.querySelector(".checkBtn")

    if (update.canGetPrime) {
        submitButton.removeAttribute('disabled')
    } else {
        submitButton.setAttribute('disabled', true)
    }

    // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unionpay', 'unknown']
    // if (update.cardType === 'visa') {
        // Handle card type visa.
    // }
})


// submit 對應動作
function submitBillFrame(event){
    event.preventDefault()

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()
    
    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('資料輸入異常')
        return
    }

    // Get prime
    TPDirect.card.getPrime(async (result) => {
        if (result.status !== 0) {
            alert('資料輸入異常 \n' + result.msg)
            return
        }
        // 成功，連接後端
        let res = await setOrder(result.card.prime)
        if (res.error){
            let target = document.querySelector(".checkFrame")
            let msg = document.createElement("div")
            msg.classList.add("checkPrice")
            msg.classList.add("checkPrice")
            msg.textContent = res.message
            target.appendChild(msg)
            return
        }
        let orderId = res.data.number

        url = `/thankyou?number=${orderId}`
        linkToUrl(url)
    })
}