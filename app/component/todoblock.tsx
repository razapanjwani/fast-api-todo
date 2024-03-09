import { useState } from "react"
import { myGetCookie } from "../../utils/authhelper"
import { URL } from "../../utils/utils"
import { useRouter } from "next/navigation"
import { Trash2 } from 'lucide-react';

const TodoBlock = ({ todo, deleteFunc, updateFunc, updateId }) => {
    const router = useRouter()


    return (
        <>
            <li className="flex flex-col md:flex-row space-y-4 md:space-y-0 justify-between md:text-start bg-white p-4 my-2 rounded-xl">
                <div className="flex space-x-4">
                    <input type="checkbox" className="" />
                    <label htmlFor="todo" className="">
                        <h4 className="md:text-2xl text-xl uppercase font-bold">{todo.title}</h4>
                        <p className="md:text-xl text-lg text-orange-800 font-medium">{todo.description}</p>
                    </label>
                </div>
                <div className="flex justify-end md:justify-normal  md:space-x-7 space-x-3">
                    <button onClick={() => { updateFunc(true); updateId(todo.id) }} className=" bg-red-800 text-white px-6 flex-shrink-0">edit</button>
                    <button onClick={() => { deleteFunc(todo.id) }}><Trash2 /></button>
                </div>
            </li>
        </>
    )
}
export default TodoBlock