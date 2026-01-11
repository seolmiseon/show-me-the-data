export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-black text-white p-4">
      <div className="text-center space-y-6">
        {/* 로고 / 타이틀 영역 */}
        <h1 className="text-5xl md:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
          Show Me The Data
        </h1>
        
        {/* 한 줄 소개 */}
        <p className="text-xl md:text-2xl text-gray-400 font-light">
          AI Business Dashboard Solution
        </p>

        {/* 뱃지 */}
        <div className="inline-block mt-8 px-6 py-2 border border-gray-800 rounded-full bg-gray-900">
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span className="text-sm text-gray-300 font-mono">2026 Fast Builderthon • Coming Soon</span>
          </span>
        </div>
      </div>
    </main>
  );
}