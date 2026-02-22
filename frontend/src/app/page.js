"use client";
import { useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, ArrowRight, BookOpen, X, Clock, User, Info, CheckCircle } from 'lucide-react';

export default function Home() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [selectedCourse, setSelectedCourse] = useState(null);
    const [courseDetails, setCourseDetails] = useState(null);
    const [hasSearched, setHasSearched] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [saveStatus, setSaveStatus] = useState('');

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setIsLoading(true);
        setHasSearched(true);
        setResults([]);
        try {
            const res = await fetch('http://localhost:8000/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, top_k: 12 })
            });
            const data = await res.json();
            setResults(data);
        } catch (err) {
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const loadDetails = async (courseCode) => {
        setCourseDetails(null);
        setSaveStatus('');
        try {
            const res = await fetch(`http://localhost:8000/course/${encodeURIComponent(courseCode)}/details`);
            const data = await res.json();
            setCourseDetails(data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleSaveCourse = async () => {
        if (!selectedCourse) return;
        setIsSaving(true);
        setSaveStatus('');
        try {
            const res = await fetch('http://localhost:8000/planner/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: 'test_user', course_code: selectedCourse.code })
            });
            const data = await res.json();
            if (data.status === 'success' || data.status === 'already saved') {
                setSaveStatus('saved');
                setTimeout(() => setSaveStatus(''), 3000);
            } else {
                setSaveStatus('error');
            }
        } catch (err) {
            console.error(err);
            setSaveStatus('error');
        } finally {
            setIsSaving(false);
        }
    };

    const containerVariants = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: { staggerChildren: 0.1 }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 15 },
        show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 100, damping: 20 } }
    };

    return (
        <div className="min-h-screen bg-[#F6F4F0] text-neutral-900 selection:bg-nyu-light selection:text-white">

            {/* Minimal Header */}
            <header className="fixed top-0 w-full bg-[#F6F4F0]/80 backdrop-blur-md z-40 border-b border-neutral-300">
                <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 bg-nyu"></div>
                        <h1 className="text-sm font-bold tracking-[0.2em] uppercase text-nyu">Academic Archive</h1>
                    </div>
                    <nav>
                        <Link href="/planner" className="text-xs font-bold tracking-widest uppercase text-neutral-500 hover:text-nyu transition-colors decoration-1 hover:underline underline-offset-4">
                            My Planner
                        </Link>
                    </nav>
                </div>
            </header>

            <main className="pt-32 pb-24 px-6 max-w-7xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
                    className="mb-20 max-w-4xl"
                >
                    <h2 className="font-serif text-6xl md:text-8xl text-neutral-900 leading-[0.9] tracking-tighter mb-8">
                        Discover your <br /><span className="italic text-nyu font-light">curriculum.</span>
                    </h2>

                    <form onSubmit={handleSearch} className="relative group mt-12">
                        <div className="absolute left-0 top-1/2 -translate-y-1/2 text-neutral-300 group-focus-within:text-nyu transition-colors duration-500">
                            <Search size={32} strokeWidth={1.5} />
                        </div>
                        <input
                            type="text"
                            className="w-full bg-transparent border-b-2 border-neutral-300 focus:border-nyu py-6 pl-12 pr-12 text-2xl md:text-4xl font-serif outline-none placeholder:text-neutral-300 text-nyu-dark transition-all duration-500"
                            placeholder="e.g. History of Renaissance Art"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !query.trim()}
                            className="absolute right-0 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-nyu disabled:opacity-30 transition-colors"
                        >
                            <ArrowRight size={32} strokeWidth={1.5} />
                        </button>
                    </form>
                </motion.div>

                {/* Loading State */}
                {isLoading && (
                    <div className="flex flex-col items-center justify-center py-20 opacity-50">
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                            className="w-12 h-12 border-t-2 border-r-2 border-nyu rounded-full mb-4"
                        />
                        <p className="font-serif text-xl animate-pulse text-nyu">Consulting neural archives...</p>
                    </div>
                )}

                {/* Results Grid - High Contrast Brutalist Cards */}
                <AnimatePresence>
                    {!isLoading && hasSearched && results.length > 0 && (
                        <motion.section
                            variants={containerVariants}
                            initial="hidden"
                            animate="show"
                            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                        >
                            {results.map((course) => (
                                <motion.div
                                    key={course.code}
                                    variants={itemVariants}
                                    onClick={() => {
                                        setSelectedCourse(course);
                                        loadDetails(course.code);
                                    }}
                                    className="group cursor-pointer bg-white border border-neutral-300 p-6 flex flex-col h-full hover:border-nyu transition-colors duration-300 relative overflow-hidden"
                                >
                                    <div className="absolute top-0 right-0 w-2 h-2 bg-nyu opacity-0 group-hover:opacity-100 transition-opacity"></div>

                                    <div className="flex justify-between items-start mb-6">
                                        <span className="font-mono text-xs font-bold bg-neutral-100 text-neutral-600 px-2 py-1 uppercase tracking-wider">
                                            {course.code}
                                        </span>
                                        <span className="font-mono text-xs text-emerald-600 bg-emerald-50 px-2 py-1 font-bold">
                                            {(course.similarity * 100).toFixed(1)}% MATCH
                                        </span>
                                    </div>

                                    <h3 className="font-serif text-2xl font-medium leading-tight mb-4 group-hover:text-nyu transition-colors">
                                        {course.name}
                                    </h3>

                                    <p className="text-neutral-500 text-sm leading-relaxed line-clamp-3 mb-6 flex-grow font-sans">
                                        {course.description}
                                    </p>

                                    <div className="pt-4 border-t border-neutral-100 flex items-center justify-between text-xs font-bold text-neutral-400 group-hover:text-nyu transition-colors uppercase tracking-widest mt-auto">
                                        <span>View Syllabus </span>
                                        <ArrowRight size={14} />
                                    </div>
                                </motion.div>
                            ))}
                        </motion.section>
                    )}
                </AnimatePresence>

                {!isLoading && hasSearched && results.length === 0 && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="py-20 text-center text-neutral-400 border border-neutral-200 border-dashed">
                        <p className="font-serif text-2xl">No semantic matches found in the archives.</p>
                    </motion.div>
                )}
            </main>

            {/* Modal - Elegant Slide-over or Massive Overlay */}
            <AnimatePresence>
                {selectedCourse && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-50 bg-[#F6F4F0]/95 backdrop-blur-xl flex items-center justify-center p-4 md:p-8"
                    >
                        <motion.div
                            initial={{ y: 50, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            exit={{ y: 20, opacity: 0 }}
                            transition={{ type: "spring", damping: 25, stiffness: 200 }}
                            className="bg-white border border-neutral-300 w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl relative"
                        >
                            <button
                                onClick={() => { setSelectedCourse(null); setCourseDetails(null); }}
                                className="absolute top-6 right-6 p-2 text-neutral-400 hover:text-nyu bg-neutral-100 hover:bg-nyu/10 rounded-full transition-all z-10"
                            >
                                <X size={20} strokeWidth={2} />
                            </button>

                            <div className="flex-1 overflow-y-auto p-8 md:p-12">
                                <div className="flex items-center gap-3 mb-4">
                                    <span className="font-mono text-sm font-bold text-nyu tracking-widest uppercase border-b border-nyu/30 pb-1">
                                        {selectedCourse.code}
                                    </span>
                                    <span className="font-sans text-xs text-neutral-500 px-3 py-1 bg-neutral-100 rounded-full">
                                        {selectedCourse.subject}
                                    </span>
                                </div>

                                <h2 className="font-serif text-4xl md:text-5xl lg:text-6xl font-medium leading-[1.1] text-neutral-900 mb-8 max-w-3xl">
                                    {selectedCourse.name}
                                </h2>

                                <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                                    <div className="lg:col-span-2 space-y-8">
                                        <div>
                                            <h3 className="flex items-center gap-2 font-mono text-xs tracking-widest uppercase text-neutral-400 mb-4">
                                                <Info size={14} /> Course Synopsis
                                            </h3>
                                            <p className="font-serif text-xl leading-relaxed text-neutral-700">
                                                {selectedCourse.description}
                                            </p>
                                        </div>
                                    </div>

                                    <div className="lg:col-span-1 border-t lg:border-t-0 lg:border-l border-neutral-200 pt-8 lg:pt-0 lg:pl-8 space-y-8">
                                        <div>
                                            <h3 className="flex items-center gap-2 font-mono text-xs tracking-widest uppercase text-neutral-400 mb-4">
                                                <BookOpen size={14} /> Real-Time Status
                                            </h3>

                                            {courseDetails ? (
                                                <div className="space-y-6">
                                                    <div>
                                                        <div className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest mb-1">Status</div>
                                                        <div className="font-sans font-medium text-sm text-nyu">{courseDetails.live_status}</div>
                                                    </div>
                                                    <div>
                                                        <div className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest mb-1">Semesters</div>
                                                        <div className="font-sans text-sm text-neutral-700">{courseDetails.available_semesters.join(', ')}</div>
                                                    </div>
                                                    <div>
                                                        <div className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest mb-1">Professors</div>
                                                        <div className="font-sans text-sm text-neutral-700">{courseDetails.professors.join(', ')}</div>
                                                    </div>
                                                    <div>
                                                        <div className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest mb-1">Prerequisites</div>
                                                        <div className="font-sans text-sm text-neutral-700 bg-neutral-100 p-2 border-l-2 border-neutral-300">{courseDetails.prerequisites}</div>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="space-y-4">
                                                    {[1, 2, 3, 4].map(i => (
                                                        <div key={i} className="animate-pulse">
                                                            <div className="h-2 w-16 bg-neutral-200 mb-2"></div>
                                                            <div className="h-4 w-full bg-neutral-100"></div>
                                                        </div>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-neutral-50 px-8 py-6 border-t border-neutral-200 flex flex-col sm:flex-row justify-between items-center gap-4">
                                <button className="w-full sm:w-auto flex items-center justify-center gap-2 font-mono text-xs font-bold tracking-widest uppercase px-6 py-4 border border-neutral-300 text-neutral-600 hover:bg-nyu hover:text-white transition-colors duration-300">
                                    <CheckCircle size={16} /> Rate highly relevant
                                </button>
                                <button
                                    onClick={handleSaveCourse}
                                    disabled={isSaving}
                                    className="w-full sm:w-auto flex items-center justify-center gap-2 font-mono text-xs font-bold tracking-widest uppercase px-8 py-4 bg-nyu text-white hover:bg-nyu-dark transition-colors duration-300 disabled:opacity-50"
                                >
                                    {saveStatus === 'saved' ? <><CheckCircle size={16} /> Saved!</> : <><BookOpen size={16} /> Save to Planner</>}
                                </button>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
