"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from 'framer-motion';
import { Trash2, ArrowLeft } from 'lucide-react';

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function Planner() {
    const { data: session, status } = useSession();
    const router = useRouter();

    const [savedCourses, setSavedCourses] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (status === 'unauthenticated') {
            router.push('/login');
        } else if (status === 'authenticated' && session?.user?.email) {
            fetchPlanner(session.user.email);
        }
    }, [status, session]);

    const fetchPlanner = async (userEmail) => {
        try {
            const res = await fetch(`http://localhost:8000/planner/${encodeURIComponent(userEmail)}`);
            const data = await res.json();
            setSavedCourses(data);
        } catch (err) {
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleRemove = async (courseCode) => {
        try {
            await fetch('http://localhost:8000/planner/remove', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: session.user.email, course_code: courseCode })
            });
            setSavedCourses(prev => prev.filter(c => c.code !== courseCode));
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="min-h-screen bg-[#F6F4F0] text-neutral-900 selection:bg-nyu-light selection:text-white">
            <header className="fixed top-0 w-full bg-[#F6F4F0]/80 backdrop-blur-md z-40 border-b border-neutral-300">
                <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-2 group">
                        <ArrowLeft size={16} className="text-neutral-400 group-hover:text-nyu transition-colors" />
                        <h1 className="text-sm font-bold tracking-[0.2em] uppercase text-neutral-400 group-hover:text-nyu transition-colors">Academic Archive</h1>
                    </Link>
                    <nav>
                        <span className="text-xs font-bold tracking-widest uppercase text-nyu decoration-1 underline underline-offset-4">
                            My Planner
                        </span>
                    </nav>
                </div>
            </header>

            <main className="pt-32 pb-24 px-6 max-w-7xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
                    className="mb-16 flex flex-col md:flex-row md:items-end justify-between gap-8 border-b border-neutral-300 pb-8"
                >
                    <div>
                        <h2 className="font-serif text-5xl md:text-7xl text-neutral-900 leading-[0.9] tracking-tighter mb-4">
                            Your <span className="italic text-nyu font-light">Planner.</span>
                        </h2>
                        <p className="font-sans text-neutral-500 max-w-md">
                            Curated courses marked for future enrollment.
                        </p>
                    </div>
                </motion.div>

                {isLoading ? (
                    <div className="flex flex-col items-center justify-center py-20 opacity-50">
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                            className="w-12 h-12 border-t-2 border-r-2 border-nyu rounded-full mb-4"
                        />
                        <p className="font-serif text-xl animate-pulse text-nyu">Retrieving records...</p>
                    </div>
                ) : savedCourses.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <AnimatePresence>
                            {savedCourses.map(course => (
                                <motion.div
                                    key={course.code}
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.95 }}
                                    className="bg-white border border-neutral-300 p-6 flex flex-col relative group"
                                >
                                    <div className="flex justify-between items-start mb-6">
                                        <span className="font-mono text-xs font-bold bg-neutral-100 text-neutral-600 px-2 py-1 uppercase tracking-wider">
                                            {course.code}
                                        </span>
                                        <button
                                            onClick={() => handleRemove(course.code)}
                                            className="text-neutral-300 hover:text-red-500 transition-colors tooltip"
                                            title="Remove from planner"
                                        >
                                            <Trash2 size={18} strokeWidth={1.5} />
                                        </button>
                                    </div>
                                    <h3 className="font-serif text-2xl font-medium leading-tight mb-4 group-hover:text-nyu transition-colors">
                                        {course.name}
                                    </h3>
                                    <p className="text-neutral-500 text-sm leading-relaxed line-clamp-3 font-sans">
                                        {course.description}
                                    </p>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>
                ) : (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="py-32 text-center"
                    >
                        <h3 className="font-serif text-3xl md:text-4xl text-neutral-400 mb-4 tracking-tight">Your planner is empty.</h3>
                        <p className="text-neutral-400 max-w-sm mx-auto mb-8 font-sans">
                            Consult the archives and curate your curriculum for upcoming semesters.
                        </p>
                        <Link href="/">
                            <button className="font-mono text-xs font-bold tracking-widest uppercase px-8 py-4 bg-nyu text-white hover:bg-nyu-dark transition-colors duration-300">
                                Return to Search
                            </button>
                        </Link>
                    </motion.div>
                )}
            </main>
        </div>
    );
}
