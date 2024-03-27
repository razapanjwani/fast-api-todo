"use client"
import { useEffect, useState, useMemo } from "react"
import { useRouter } from "next/navigation"
import { URL } from "../../utils/utils"
import { myGetCookie } from "../../utils/authhelper"
import TodoBlock from "./todoblock"
import { hasCookie } from "cookies-next"
import Modal from "./model"
const Todo = () => {
    const router = useRouter()
    const [todos, setTodos] = useState([])
    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")
    const [updatedTitle, setUpdatedTitle] = useState("")
    const [updateddescription, setUpdatedDescription] = useState("")
    const [showModal, setShowModal] = useState(false)
    const [myId, setMyId] = useState("")


    const validate_refresh_token = async () => {
        const formData = new URLSearchParams();
        const tokens = await myGetCookie()
        if (tokens.refresh_token) {
            formData.append('refresh_token', tokens.refresh_token)
        }
        try {
            const response = await fetch(`${URL}/api/token`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            })
            if (response.ok) {
                const data = await response.json();
                if (data) {
                    const newAccessToken = data.access_token;
                    return newAccessToken;
                }
            } else if (response.status == 500) {
                router.refresh()
            }
        } catch (error) {

        }
    }

    const getTodos = async () => {
        const accessToken = await myGetCookie()

        console.log(accessToken, "accessToken");

        try {
            const res = await fetch(`${URL}/api/todos`, {
                headers: {
                    'Authorization': `Bearer ${accessToken.access_token}`,
                    'Content-Type': 'application/json',
                },
            })
            if (res.ok) {
                const data = await res.json()
                setTodos(data)
            } else if (res.status == 401) {
                const newToken = await validate_refresh_token()
                try {
                    const retryRes = await fetch(`${URL}/api/todos`, {
                        headers: {
                            'Authorization': `Bearer ${newToken}`,
                            'Content-Type': 'application/json',
                        }

                    })
                    if (retryRes.ok) {
                        const data = await retryRes.json()
                        setTodos(data)
                    }
                } catch (error) {
                    console.log(error);
                }
            }
        } catch (error) {
            console.log(error);
        }
    }

    const createTodo = async () => {
        const accessToken = await myGetCookie()
        console.log(accessToken.access_token, "aa");


        try {
            const res = await fetch(`${URL}/api/createtodo`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${accessToken.access_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "title": title,
                    "description": description
                })
            })
            if (res.ok) {
                const data = await res.json()
                console.log(data);
                getTodos()
            } else if (res.status == 401) {
                const newToken = await validate_refresh_token()
                try {
                    const retryRes = await fetch(`${URL}/api/createtodo`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${newToken}`,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            "title": title,
                            "description": description
                        })
                    })
                    console.log("second request");
                    getTodos()

                } catch (error) {
                    console.log(error);
                }
            } else {
                console.log("could not fetch");
            }
            setTitle("")
            setDescription("")

        } catch (error) {

        }
    }
    const deleteTodo = async (id) => {
        try {
            const accessToken = await myGetCookie()
            const res = await fetch(`${URL}/api/deletetodo/?todo_id=${id}`, {
                method: "DELETE",
                headers: {
                    'Authorization': `Bearer ${accessToken.access_token}`
                }
            })
            if (res.ok) {
                const data = await res.json()
                console.log(data);
                getTodos()
            } else if (res.status == 401) {
                try {
                    const newToken = await validate_refresh_token()
                    const res = await fetch(`${URL}/api/deletetodo/?todo_id=${id}`, {
                        method: "DELETE",
                        headers: {
                            'Authorization': `Bearer ${newToken}`
                        }
                    })
                    getTodos()
                } catch (error) {

                }
            }
        } catch (error) {
            console.log(error);

        }
    }
    const updateTodo = async (id) => {
        try {
            const accessToken = await myGetCookie()
            const res = await fetch(`${URL}/api/updatetodo/?todo_id=${id}`, {
                method: "PUT",
                headers: {
                    'Authorization': `Bearer ${accessToken.access_token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "title": updatedTitle,
                    "description": updateddescription
                })
            })
            if (res.ok) {
                const data = await res.json()
                setShowModal(false)
                setUpdatedTitle("")
                setUpdatedDescription("")
                console.log(id);

                getTodos()
            } else if (res.status == 401) {
                const newToken = await validate_refresh_token()
                try {
                    const res = await fetch(`${URL}/api/updatetodo/?todo_id=${id}`, {
                        method: "PUT",
                        headers: {
                            'Authorization': `Bearer ${newToken}`,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            "title": updatedTitle,
                            "description": updateddescription
                        })
                    })
                    setShowModal(false)
                    setUpdatedTitle("")
                    setUpdatedDescription("")
                    console.log(id);
                    getTodos()
                } catch (error) {

                }
            }
        } catch (error) {

        }
    }
    useEffect(() => {
        if (hasCookie("access_token")) {
            getTodos();
        }
    }, []); // Empty dependency array means this effect runs once when the component mounts


    return (
        <>
            <div className="max-w-xs md:max-w-xl mx-auto bg-gray-50 shadow-lg rounded-lg overflow-hidden mt-16 p-5 ">
                <div className="px-4 py-2">
                    <h1 className="text-gray-800 font-bold text-2xl md:text-3xl uppercase m-2">To-Do List</h1>
                </div>
                <form className="w-full max-w-xl mx-auto px-4 py-2 space-y-7" onSubmit={(e) => { e.preventDefault(); createTodo() }}>
                    <div className="flex flex-col items-center space-y-5">
                        <input
                            className="md:text-lg text-base appearance-none bg-transparent border-2 border-teal-500 w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none"
                            type="text" placeholder="Add a task" onChange={(e) => { setTitle(e.target.value) }} value={title} />
                        <input
                            className="md:text-lg text-base appearance-none bg-transparent w-full border-2 border-teal-500 text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none"
                            type="text" placeholder="Add description" onChange={(e) => { setDescription(e.target.value) }} value={description} />
                    </div>
                    <div className="">
                        <button
                            className="flex-shrink-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 md:text-lg text-base border-4 text-white py-1 md:px-10 px-5 rounded"
                            type="submit">
                            Add
                        </button>
                    </div>
                </form>
                <div>
                    {todos && todos.map((todo, index) => {
                        return (
                            <>
                                <ul className="flex flex-col">
                                    <TodoBlock key={index} todo={todo} deleteFunc={deleteTodo} updateFunc={setShowModal} updateId={setMyId} />
                                </ul>

                            </>
                        )
                    })}
                </div>
                <div className="absolute z-10">
                    <form action="" onSubmit={(e) => { e.preventDefault(); updateTodo(myId) }} className={`${showModal ? "block" : "hidden"} w-full px-4 py-2 space-y-7`}>
                        <Modal title={updatedTitle} description={updateddescription} updatedTitle={setUpdatedTitle} updatedDescription={setUpdatedDescription} showModal={setShowModal} />
                    </form>
                </div>
            </div>

        </>
    )
}
export default Todo