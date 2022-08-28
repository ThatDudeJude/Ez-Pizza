
const Pizza = ({data, toppings, name, checkPrice, getForm}) => {

    let [availToppings, updateToppings] = React.useReducer(toppingsReducer, {'toppings': toppings, 'choices': {
        'topping1': '',
        'topping2':'',
        'topping3':''
    }});

    let [total, updateTotal] = React.useState('00.00');    
    let smallRef = React.useRef();
    let largeRef = React.useRef();

    React.useEffect(() => {
        updateToppings({type:'SET_TOPPINGS', payload: {'toppings': toppings, 'choices': availToppings.choices}})
        // smallRef.current.checked = false;
        // largeRef.current.checked = false;
    }, [toppings]);
    
    // console.log('tops', toppings, 'avail', availToppings.toppings, 'choices', availToppings.choices);

    

    const onSelectToppingOne = React.useCallback(() => {
        const value = document.querySelector('#toppingOne').value;        
        const choices = {...availToppings.choices, 'topping1': value};
        // console.log('choices change 1', choices)
        updateToppings({type:'UPDATE_AVAILABLE_TOPPINGS', payload: {toppings, choices}});
    }, [availToppings]);

    const getTotalPrice = React.useCallback(() => {
        let choices = [smallRef, largeRef];
        let pizzaTotalPrice = 0;

        choices.forEach(choice => {
            if (choice.current.checked) {
                pizzaTotalPrice += parseFloat(choice.current.value);
            }
        });
        
        updateTotal(toDecimalPlaces(String(pizzaTotalPrice), 2).padStart(6));
               
        checkPrice(pizzaTotalPrice != 0)
        checkPrice((smallRef.current.checked || largeRef.current.checked))
        getForm(document.querySelector(name.includes('Regular')? "#regular-form": "#sicillian-form"))
    }, [])

    const onSelectToppingTwo = React.useCallback(() => {
        const value = document.querySelector('#toppingTwo').value;
        const choices = {...availToppings.choices, 'topping2': value};
        // console.log('choices change 2', choices)
        updateToppings({type:'UPDATE_AVAILABLE_TOPPINGS', payload: {toppings, choices}});
    }, [availToppings]);

    const onSelectToppingThree = React.useCallback(() => {
        const value = document.querySelector('#toppingThree').value;
        const choices = {...availToppings.choices, 'topping3': value};
        // console.log('choices change 3', choices)
        updateToppings({type:'UPDATE_AVAILABLE_TOPPINGS', payload: {toppings, choices}});
    }, [availToppings]);

    

    return (
      <div>          
                          <form action="/shop/add/pizza/" method="post" className='col-12' id={name.includes('Regular')? "regular-form": "sicillian-form"}>   

                            <CSRF />

                          <h3 className="mb-4 text-center">{data.delicacy}</h3>  
                          <table className="table table-dark" id="table-form">                                        
                                        <tbody>
                                            
                                                        
                              {data && /[123]/.test(data.delicacy) &&
                              <tr>                                  
                                  <td className="text-center"><label htmlFor="toppingOne" className="form-label fs-4 px-0">{name.includes('Regular') ? 'Topping' : 'Item'}</label></td>                                                                    
                                  <td colSpan="2">
                                      <input type="text" className="form-control fs-4 fs topping" name="toppingOne" id="toppingOne" list="topping1-options" onChange={() => onSelectToppingOne()} />
                                  <datalist  id="topping1-options">
                                  {availToppings.toppings? availToppings.toppings.map(topping => (<option key={topping.id}  value={topping.name} />)): ''}                                                                        
                                  </datalist>
                                  </td>                                  
                              </tr>
                                }

                                {data && /[23]/.test(data.delicacy) &&    
                            <tr>                                
                                <td className="text-center"><label htmlFor="toppingTwo" className="form-label fs-4 px-0">{name.includes('Regular') ? 'Topping' : 'Item'}</label></td>
                                <td colSpan="2"><input type="text" className="form-control fs-4 topping" name="toppingTwo" id="toppingTwo" list="topping2-options" onChange={() => onSelectToppingTwo()} />
                                <datalist  id="topping2-options">
                                {availToppings.toppings? availToppings.toppings.map(topping => (<option key={topping.id}  value={topping.name} />)): ''}                                                                        
                                </datalist>
                                </td>                                
                                
                            </tr>
                                }

                                {data && /[3]/.test(data.delicacy) &&
                                <tr>                                  
                                  <td className="text-center"><label htmlFor="toppingThree" className="form-label fs-4 px-0">{name.includes('Regular') ? 'Topping' : 'Item'} </label></td>
                                  <td colSpan="2"><input type="text" className="form-control fs-4 topping" name="toppingThree" id="toppingThree" list="topping3-options"onChange={() => onSelectToppingThree()} />
                                  <datalist  id="topping3-options">
                                    
                                  {availToppings.toppings? availToppings.toppings.map(topping => (<option key={topping.id}  value={topping.name} />)): ''}                                                                        
                                  </datalist>
                                  </td>                                  
                                </tr>
                                }

                              <tr>
                                  <td className="text-center">
                                      <input ref={smallRef} className="form-check-input" type="checkbox" name="small" id="small" onChange={() => getTotalPrice()} value={data? data.small: '00.00'} />
                                       </td>
                                  <td className="text-center">
                                      <label className="form-check-label fs-4" htmlFor="small">Small</label>                                                            </td>
                                  <td className="text-end"><p className="price fs-4 px-1">
                                       {data && data.small}
                                  </p></td>                                  
                              </tr>
                            <tr>
                                  <td className="text-center"><input ref={largeRef} className="form-check-input" type="checkbox" name="large" id="large" onChange={() => getTotalPrice()} value={data? data.large: '00.00'} /> </td>
                                  <td className="text-center"><label className="form-check-label fs-4" htmlFor="large">Large</label>                                                            </td>
                                  <td className="text-end"><p className="price fs-4 px-1">
                                       {data && data.large}
                                  </p></td>                                  
                              </tr>
                              
                              
                                <tr>                                    
                                    <td colSpan="2">
                                        <span className="fs-4" style={{fontFamily: 'Arial'}}>Total ($)</span>
                                    </td>                                  
                                    <td className="text-end">
                                        <span className="fs-4 px-1">= {total}</span></td>
                                </tr>   
                                </tbody>
                            </table>                             
                          </form>              
      </div>
    )
  }



export default Pizza