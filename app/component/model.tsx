import { X } from 'lucide-react';


const Modal = ({ title, description, updatedTitle, updatedDescription, showModal }) => {
    return (
        <>
            {/* <div className="flex flex-col items-center space-y-5">
                <button type="button" onClick={() => {
                    showModal(false)
                }}>close</button>
                <input className="text-lg appearance-none bg-transparent border-2 border-teal-500 w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" name="" id="" value={title} onChange={(e) => { updatedTitle(e.target.value) }} />
                <input type="text" className="text-lg appearance-none bg-transparent border-2 border-teal-500 w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" name="" id="" value={description} onChange={(e) => { updatedDescription(e.target.value) }} />
                <button type="submit" className="flex-shrink-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 text-lg border-4 text-white py-1 px-10 rounded">update</button>
            </div> */}
            <div className="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
                <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                    <div className="flex min-h-full justify-center p-4 text-center items-center sm:p-0">
                        <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                            <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                                <div className="md:flex md:flex-col">
                                    <div className="mt-3 sm:ml-4 sm:mt-0 sm:text-left">
                                        <div className='flex justify-between items-center mb-3'>
                                            <h3 className="text-gray-900 uppercase font-bold md:text-3xl text-xl my-3" id="modal-title">update todo</h3>
                                            <button type='button' onClick={() => { showModal(false) }}>
                                                <X />
                                            </button>
                                        </div>
                                        <div className="flex flex-col items-center space-y-3">
                                            <input
                                                className="text-lg appearance-none bg-transparent border-2 border-red-500 w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none"
                                                type="text" placeholder="Update The Task" onChange={(e) => { updatedTitle(e.target.value) }} value={title} />
                                            <input
                                                className="text-lg appearance-none bg-transparent w-full border-2 border-red-500 text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none"
                                                type="text" placeholder="Update The Description" onChange={(e) => { updatedDescription(e.target.value) }} value={description} />
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                                <button type="submit" className="inline-flex  justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto uppercase">update</button>
                                {/* <button type="button" className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto">Cancel</button> */}
                            </div>
                        </div>
                    </div>
                </div>
            </div >

        </>
    )
}
export default Modal