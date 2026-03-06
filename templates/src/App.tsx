/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { Battery, Signal, Wifi, X } from 'lucide-react';
import { AnimatePresence, motion } from 'motion/react';
import { useState } from 'react';

export default function App() {
  const [showInput, setShowInput] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [modalResult, setModalResult] = useState<string | null>(null);

  const classify = async () => {
    if (!showInput) {
      setShowInput(true);
      return;
    }

    if (!inputValue.trim()) return;

    try {
      const response = await fetch('/classify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ my_test_data: inputValue }),
      });
      const data = await response.json();
      setModalResult(data.result);
    } catch (error) {
      console.error('Error during classification:', error);
      setModalResult('오류가 발생했습니다.');
    }
  };

  const closeModal = () => {
    setModalResult(null);
    setInputValue('');
    setShowInput(false);
  };

  return (
    <div className="relative h-screen w-full overflow-hidden bg-green-100 font-sans text-white">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <img
          src="https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?q=80&w=2670&auto=format&fit=crop"
          alt="Recycling bins"
          className="h-full w-full object-cover"
          referrerPolicy="no-referrer"
        />
        {/* Overlay gradient for better text readability */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/10 via-transparent to-black/20" />
      </div>

      {/* Status Bar (Simulated) */}
      <div className="absolute top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-3 text-white drop-shadow-md">
        <span className="text-sm font-semibold">9:41</span>
        <div className="flex items-center gap-1.5">
          <Signal className="h-4 w-4 fill-current" />
          <Wifi className="h-4 w-4" />
          <Battery className="h-4 w-4 fill-current" />
        </div>
      </div>

      {/* Top Logo */}
      <div className="absolute top-0 left-0 right-0 z-40 flex justify-center pt-3">
        <span className="font-script text-2xl text-white drop-shadow-md">emo</span>
      </div>

      {/* Main Content */}
      <main className="relative z-10 flex h-full flex-col items-center justify-center px-4">

        {/* RECYCLE Badge */}
        <motion.div
          initial={{ scale: 0.9, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="relative mb-2 flex flex-col items-center"
        >
          <div className="relative flex items-center justify-center rounded-[3rem] bg-white px-8 py-6 shadow-xl sm:px-12 sm:py-10">
            {/* Slight arch effect using CSS transform if desired, but keeping it clean for now */}
            <h1 className="font-display text-6xl tracking-tighter text-[#2E7D32] sm:text-8xl">
              RECYCLE
            </h1>
          </div>
        </motion.div>

        {/* Subtitle */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.8 }}
          className="mt-4"
        >
          <span className="font-sans text-sm text-white/90 drop-shadow-sm">by </span>
          <span className="font-script text-xl text-white drop-shadow-sm">emo</span>
        </motion.div>

      </main>

      {/* Footer Actions */}
      <div className="absolute bottom-0 left-0 right-0 z-20 flex flex-col items-center pb-8 px-6">
        <p className="mb-6 text-center text-xs font-medium text-gray-600/80 mix-blend-multiply">
          By tapping "{showInput ? "Submit" : "Get me in"}" you're<br />

        </p>

        {showInput && (
          <motion.div
            initial={{ opacity: 0, y: 20, height: 0 }}
            animate={{ opacity: 1, y: 0, height: 'auto' }}
            className="mb-4 w-full max-w-xs"
          >
            <input
              type="text"
              placeholder="Enter recycle item"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="w-full rounded-full bg-white/90 px-6 py-4 text-black shadow-lg outline-none backdrop-blur-sm transition-all focus:ring-2 focus:ring-[#4A6FFF]"
              autoFocus
            />
          </motion.div>
        )}

        <motion.button
          onClick={classify}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full max-w-xs rounded-full bg-gradient-to-r from-[#43A047] to-[#66BB6A] py-4 text-lg font-semibold text-white shadow-lg shadow-green-900/30 transition-all hover:shadow-green-900/40 active:shadow-green-900/20"
        >
          {showInput ? "Submit" : "Get me in"}
        </motion.button>

        {/* Home Indicator */}
        <div className="mt-6 h-1 w-32 rounded-full bg-white/30" />
      </div>

      {/* Modal / Alert Replacement */}
      <AnimatePresence>
        {modalResult && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 px-4 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              className="relative w-full max-w-sm rounded-[2rem] bg-white p-6 shadow-2xl"
            >
              <button
                onClick={closeModal}
                className="absolute right-4 top-4 rounded-full bg-gray-100 p-2 text-gray-500 hover:bg-gray-200"
              >
                <X className="h-5 w-5" />
              </button>

              <div className="mt-4 flex flex-col items-center text-center">
                <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
                  <span className="text-3xl">♻️</span>
                </div>
                <h3 className="mb-2 font-display text-2xl font-bold text-gray-800">
                  분류 결과
                </h3>
                <p className="mb-6 text-xl text-gray-600">
                  {modalResult}
                </p>
                <button
                  onClick={closeModal}
                  className="w-full rounded-full bg-[#43A047] py-3 text-lg font-semibold text-white shadow-lg shadow-green-900/20 transition-all hover:bg-[#388E3C] active:shadow-none"
                >
                  확인
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
