import { useState, useRef, useEffect } from "react"
import Section_4 from "./Section_4"

function Formulario() {
  const [valueInner, setValueInner] = useState({
    t_1: '',
    p_1: '',
    q_ent: '',
    pr: '',
    t_ent: '',
    E_ent: ''
  })
  const [errors, setErrors] = useState({
    t_1: '',
    p_1: '',
    q_ent: '',
    pr: '',
    t_ent: '',
  })
  const [dataApi, setDataApi] = useState(null)
  const [loading, setLoading] = useState(false)
  const section4Ref = useRef(null)
  const formulario = useRef(null)
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);
  const URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000/'
  useEffect(() => {
    const allFieldsFilled = Object.values(valueInner).every(value => value !== '');
    setIsButtonDisabled(!allFieldsFilled);
  }, [valueInner]);

  const setValue = (e) =>{
    setValueInner({
      ...valueInner,
      [e.target.id]: Math.max(0,e.target.value)
    })
  }
  const validateInput = (e)=>{
    const {id,value} = e.target;
    let error='';
    if(id===t_1 && (value<15 || value>1700)){
      error='El valor debe estar entre 15 C y 1700 C'
    } else if(id===p_1 && (value<100 || value>2000)){
      error='El valor debe estar entre 100 kPa y 2000 kPa'
    } else if (id===q_ent && (value<300 || value>2000)){
      error='El valor debe estar entre 300 kJ/kg y 2000 kJ/kg'
    } else if(id===pr && (value<2 || value>30)){
      error='El valor debe estar entre 2 y 30'
    } else if(id===t_ent && (value<15)){
      error='El valor debe ser mayor a 15C'
    }
    setErrors({...errors,[id]:error})
  }
  const handleSubmit = async (e) => {
    e.preventDefault();
    const numericData = {
      pr: parseFloat(valueInner.pr),
      t_1: parseFloat(valueInner.t_1),
      p_1: parseFloat(valueInner.p_1),
      q_ent: parseFloat(valueInner.q_ent),
      t_ent: parseFloat(valueInner.t_ent),
      E_ent: parseFloat(valueInner.E_ent)
    };
    setLoading(true)
    try {
      const response = await fetch(`${URL}api/resultado/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(numericData)
      });

      const data = await response.json();
      setDataApi(data);
      setLoading(false);
    }catch(error){
      console.log(error);}

    if(section4Ref.current){
      section4Ref.current.scrollIntoView({ behavior: "smooth" })
    }
  }

  const recharge = () =>{
    setValueInner({
      t_1: '',
      p_1: '',
      q_ent: '',
      pr: '',
      t_ent: '',
      E_ent: ''
    })
    setDataApi(null)
    setLoading(false)
    if(formulario.current){
      formulario.current.scrollIntoView({ behavior: "smooth" })
    }
  }

  return (
    <>
      <section className="flex flex-col justify-center items-center my-4 bg-red-200 py-10  gap-8 w-full" ref={formulario}>
        <h2 className=" font-semibold text-2xl md:text-3xl">Ingresa los datos</h2>
        <form action="" className=" flex flex-col gap-4 border-4 py-5 px-3 sm:px-8 rounded-3xl items-start justify-center  w-full max-w-[250px] sm:max-w-[400px] border-red-800">
          <div className=" flex flex-col items-start justify-center gap-2 w-full">
            <label htmlFor="t_1" className=" text-lg font-medium">Temperatura de entrada (C) :</label>
            <input type="number" id="t_1" className=" rounded-md p-1 px-2 w-full no-arrows" inputMode="numeric" value={valueInner.t_1} onChange={setValue} min={15} max={1700} />
            {errors.t_1 && <p className="text-red-500 text-xs">{errors.t_1}</p>}
          </div>
          <div className=" flex flex-col items-start justify-center gap-2 w-full">
            <label htmlFor="p_1" className=" text-lg font-medium">Presion  de entrada (KPa) :</label>
            <input type="number" id="p_1" className=" rounded-md p-1 px-2 w-full no-arrows" inputMode="numeric" value={valueInner.p_1} onChange={setValue} min={100} max={2000}/>
            {errors.p_1 && <p className="text-red-500 text-xs">{errors.p_1}</p>}
          </div>
          <div className=" flex flex-col items-start justify-center gap-2 w-full">
            <label htmlFor="q_ent" className="text-lg font-medium" >Calor entrada en cámara de combustión (kJ/kg):</label>
            <input type="number" id="q_ent" className=" rounded-md p-1 px-2 w-full no-arrows" inputMode="numeric" value={valueInner.q_ent} onChange={setValue} min={300} max={2000}/>
            {errors.q_ent && <p className="text-red-500 text-xs">{errors.q_ent}</p>}
          </div>
          <div className=" flex flex-col items-start justify-center gap-2 w-full">
            <label htmlFor="pr" className=" text-lg font-medium">Relación de presiones:</label>
            <input type="number" id="pr" className=" rounded-md p-1 px-2 w-full no-arrows" inputMode="numeric" value={valueInner.pr} onChange={setValue} min={2} max={30}/>
            {errors.pr && <p className="text-red-500 text-xs">{errors.pr}</p>}
          </div>
          <div className=" flex flex-col items-start justify-center gap-2 w-full">
            <label htmlFor="t_ent" className=" text-lg font-medium">Temperatura de regenerador (C):</label>
            <input type="number" id="t_ent" className=" rounded-md p-1 px-2 w-full no-arrows" inputMode="numeric" value={valueInner.t_ent} onChange={setValue} min={15}/>
            {errors.t_ent && <p className="text-red-500 text-xs">{errors.t_ent}</p>}
          </div>
          <div className=" flex flex-col items-start justify-center gap-2 w-full">
            <label htmlFor="E_ent" className=" text-lg font-medium">Energia de entrada (kW):</label>
            <input type="number" id="E_ent" className=" rounded-md p-1 px-2 w-full no-arrows" inputMode="numeric" value={valueInner.E_ent} onChange={setValue}/>
          </div>
          <button className=" self-center bg-red-800 py-3 px-3 sm:px-7 rounded-lg mt-4 hover:cursor-pointer hover:scale-105 transition-all" onClick={handleSubmit} disabled={isButtonDisabled}>
            <p className=" font-medium text-white ">CALCULAR</p>
          </button>
        </form>
      </section>
      <Section_4 loading={loading} dataApi = {dataApi} referencia={section4Ref} reiniciar={recharge}/>

      
    </>
    
  )
}

export default Formulario