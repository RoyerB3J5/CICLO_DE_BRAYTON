import mecatronica from '../assets/mecatronica.svg'
import unt from '../assets/unt.png'
import fondo from '../assets/fondo.png'
function Section_1() {
  return (
    <header className="w-screen flex justify-between items-center px-2 sm:px-5 md:px-28 py-4 sm:py-10 bg-center bg-cover " style={{ backgroundImage: `url(${fondo})` }} >
      <img src={mecatronica} alt="Logo de mecatronica" className=' aspect-square w-24' />
      <div className="flex justify-center items-center py-3 md:py-6 px-2 sm:px-5 md:px-12   text-center " >
        <h1 className=" text-2xl md:text-4xl font-extrabold uppercase text-white">Ciclo Brayton</h1>  
      </div>
      <img src={unt} alt="Logo de UNT" className='w-32 hidden sm:flex' />
      
    </header>
  )
}

export default Section_1