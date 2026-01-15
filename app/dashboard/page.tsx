"use client";

import { useState, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";

type EventType = "recruit" | "order" | "work";

interface Event {
  id?: string;
  event_type: EventType;
  customer_name?: string;
  datetime?: string;
  description?: string;
  original_text: string;
  created_at: string;
  user_id?: string;
  confidence: number;
}

interface EventResponse {
  event: Event;
  analysis: string;
  tokens_used: number;
}

// API Base URL - Vercel Serverless Functions 사용
// 상대 경로로 설정하여 같은 도메인에서 API 호출
const API_BASE_URL = "/api";

export default function Dashboard() {
  const [mode, setMode] = useState<EventType>("work");
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [events, setEvents] = useState<Event[]>([]);
  const [calendarEvents, setCalendarEvents] = useState<any[]>([]);
  const [analysis, setAnalysis] = useState<string>("");

  // 모드별 색상 테마
  const modeColors = {
    recruit: {
      bg: "bg-blue-900",
      border: "border-blue-700",
      text: "text-blue-300",
      button: "bg-blue-600 hover:bg-blue-700",
      calendar: "#3b82f6",
    },
    order: {
      bg: "bg-purple-900",
      border: "border-purple-700",
      text: "text-purple-300",
      button: "bg-purple-600 hover:bg-purple-700",
      calendar: "#9333ea",
    },
    work: {
      bg: "bg-green-900",
      border: "border-green-700",
      text: "text-green-300",
      button: "bg-green-600 hover:bg-green-700",
      calendar: "#22c55e",
    },
  };

  const currentTheme = modeColors[mode];

  // 이벤트 목록 조회
  const fetchEvents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/events?event_type=${mode}`);
      const data = await response.json();
      setEvents(data.events || []);
      
      // FullCalendar 형식으로 변환
      const calEvents = (data.events || []).map((event: Event) => ({
        id: event.id,
        title: event.customer_name || "이름 없음",
        start: event.datetime || event.created_at,
        backgroundColor: currentTheme.calendar,
        borderColor: currentTheme.calendar,
        extendedProps: {
          description: event.description,
          original_text: event.original_text,
          event_type: event.event_type,
        },
      }));
      setCalendarEvents(calEvents);
    } catch (error) {
      console.error("이벤트 조회 오류:", error);
    }
  };

  // 이벤트 생성 (이메일/메시지 분석)
  const handleAnalyze = async () => {
    if (!inputText.trim()) return;

    setIsLoading(true);
    setAnalysis("");

    try {
      const response = await fetch(`${API_BASE_URL}/events`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: inputText,
          mode: mode,
          user_id: null,
        }),
      });

      const data: EventResponse = await response.json();
      
      if (data.event) {
        setAnalysis(data.analysis);
        setInputText(""); // 입력창 초기화
        await fetchEvents(); // 이벤트 목록 새로고침
      }
    } catch (error) {
      console.error("분석 오류:", error);
      setAnalysis("오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setIsLoading(false);
    }
  };

  // 이벤트 삭제
  const handleDeleteEvent = async (eventId: string) => {
    try {
      await fetch(`${API_BASE_URL}/events/${eventId}`, {
        method: "DELETE",
      });
      await fetchEvents(); // 목록 새로고침
    } catch (error) {
      console.error("삭제 오류:", error);
    }
  };

  // 초기 로드
  useEffect(() => {
    fetchEvents();
  }, [mode]);

  // 모드 변경 시 캘린더 이벤트 색상 업데이트
  useEffect(() => {
    const updatedEvents = calendarEvents.map((event) => ({
      ...event,
      backgroundColor: currentTheme.calendar,
      borderColor: currentTheme.calendar,
    }));
    setCalendarEvents(updatedEvents);
  }, [mode]);

  return (
    <div className={`min-h-screen ${currentTheme.bg} text-white`}>
      {/* 상단 헤더 */}
      <header className={`${currentTheme.border} border-b-2 p-4`}>
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold">Show Me The Data</h1>
          
          {/* 모드 전환 토글 */}
          <div className="flex gap-2">
            <button
              onClick={() => setMode("recruit")}
              className={`px-4 py-2 rounded-lg transition-colors ${
                mode === "recruit"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-700 text-gray-300 hover:bg-gray-600"
              }`}
            >
              채용
            </button>
            <button
              onClick={() => setMode("order")}
              className={`px-4 py-2 rounded-lg transition-colors ${
                mode === "order"
                  ? "bg-purple-600 text-white"
                  : "bg-gray-700 text-gray-300 hover:bg-gray-600"
              }`}
            >
              예약
            </button>
            <button
              onClick={() => setMode("work")}
              className={`px-4 py-2 rounded-lg transition-colors ${
                mode === "work"
                  ? "bg-green-600 text-white"
                  : "bg-gray-700 text-gray-300 hover:bg-gray-600"
              }`}
            >
              업무
            </button>
          </div>
        </div>
      </header>

      {/* 메인 컨텐츠 */}
      <div className="max-w-7xl mx-auto p-4 grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* 좌측: 채팅/입력창 */}
        <div className={`${currentTheme.border} border-2 rounded-lg p-6 space-y-4`}>
          <h2 className="text-xl font-bold mb-4">이메일/메시지 입력</h2>
          
          {/* 입력창 */}
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder={`예: 김철수 클라이언트: 이번 주 목요일 3시에 미팅합시다.`}
            className="w-full h-32 p-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />

          {/* 분석 버튼 */}
          <button
            onClick={handleAnalyze}
            disabled={isLoading || !inputText.trim()}
            className={`w-full py-3 rounded-lg font-semibold transition-colors ${
              isLoading || !inputText.trim()
                ? "bg-gray-600 cursor-not-allowed"
                : currentTheme.button
            }`}
          >
            {isLoading ? "분석 중..." : "분석 및 일정 등록"}
          </button>

          {/* 분석 결과 */}
          {analysis && (
            <div className={`p-4 rounded-lg bg-gray-800 ${currentTheme.border} border`}>
              <p className="text-sm">{analysis}</p>
            </div>
          )}

          {/* 이벤트 목록 */}
          <div className="mt-6">
            <h3 className="text-lg font-bold mb-3">최근 이벤트</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {events.length === 0 ? (
                <p className="text-gray-400 text-sm">등록된 이벤트가 없습니다.</p>
              ) : (
                events.slice(0, 5).map((event) => (
                  <div
                    key={event.id}
                    className={`p-3 rounded-lg bg-gray-800 ${currentTheme.border} border`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="font-semibold">
                          {event.customer_name || "이름 없음"}
                        </p>
                        <p className="text-sm text-gray-400 mt-1">
                          {event.datetime
                            ? new Date(event.datetime).toLocaleString("ko-KR")
                            : "시간 미정"}
                        </p>
                        {event.description && (
                          <p className="text-sm text-gray-300 mt-2">
                            {event.description}
                          </p>
                        )}
                      </div>
                      <button
                        onClick={() => event.id && handleDeleteEvent(event.id)}
                        className="text-red-400 hover:text-red-300 text-sm ml-2"
                      >
                        삭제
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* 우측: 캘린더 */}
        <div className={`${currentTheme.border} border-2 rounded-lg p-6`}>
          <h2 className="text-xl font-bold mb-4">캘린더</h2>
          <div className="bg-white rounded-lg p-2">
            <FullCalendar
              plugins={[dayGridPlugin, interactionPlugin]}
              initialView="dayGridMonth"
              events={calendarEvents}
              headerToolbar={{
                left: "prev,next today",
                center: "title",
                right: "dayGridMonth",
              }}
              // locale="ko" // 한국어 로케일은 별도 설치 필요
              height="auto"
              eventClick={(info) => {
                alert(
                  `이벤트: ${info.event.title}\n설명: ${info.event.extendedProps.description || "없음"}`
                );
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
