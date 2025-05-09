import { useEffect } from "react";

function Error404() {

    useEffect(() => {
        document.title = 'E not found page'
    }, [])

    return (
        <div className='h-screen flex justify-center items-center'>
            <h1 className='text-amber-600 text-[200%] p-9 border-4 rounded-[20px] border-amber-600'>
                Bro, page that you are looking for does not exist
            </h1>
        </div>
    )
}


export default Error404
