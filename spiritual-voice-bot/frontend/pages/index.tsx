import { useState, useRef, useEffect } from 'react';
import Head from 'next/head';
import { Mic, Send, Volume2, Loader2, BookOpen } from 'lucide-react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  timestamp: Date;
}

interface Citation {
  reference: string;
  text: string;
  scripture: string;
  score: number;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [language, setLanguage] = useState<'en' | 'hi'>('en');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);

    try {
      const response = await axios.post(`${API_URL}/api/text/query`, {
        query: input,
        language: language,
        include_citations: true
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.answer,
        citations: response.data.citations,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'I apologize, but I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        }
      });

      // Determine supported mime type
      const mimeType = MediaRecorder.isTypeSupported('audio/webm')
        ? 'audio/webm'
        : 'audio/mp4';

      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: mimeType });
        await sendVoiceQuery(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Failed to access microphone. Please grant permission.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const sendVoiceQuery = async (audioBlob: Blob) => {
    setIsProcessing(true);

    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'query.wav');
      formData.append('language', language);

      const response = await axios.post(`${API_URL}/api/voice/query`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob'
      });

      // Get transcription from headers
      const transcription = response.headers['x-transcription'] || 'Voice query';

      const userMessage: Message = {
        role: 'user',
        content: transcription,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, userMessage]);

      // Play audio response
      const audioUrl = URL.createObjectURL(response.data);
      const audio = new Audio(audioUrl);

      setIsPlaying(true);
      audio.onended = () => setIsPlaying(false);
      await audio.play();

      // Extract text from citations if available
      const citations = response.headers['x-citations'];
      const assistantMessage: Message = {
        role: 'assistant',
        content: 'Voice response (click to replay)',
        citations: citations ? JSON.parse(citations) : [],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Error sending voice query:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'I apologize, but I encountered an error processing your voice query.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <>
      <Head>
        <title>Spiritual Voice Bot - Sanatan Dharma AI Companion</title>
        <meta name="description" content="Voice-enabled spiritual companion based on Sanatan Dharma" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-orange-200">
          <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-amber-600 rounded-full flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Spiritual Voice Bot</h1>
                <p className="text-sm text-gray-600">Sanatan Dharma AI Companion</p>
              </div>
            </div>

            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as 'en' | 'hi')}
              className="px-4 py-2 border border-orange-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="en">English</option>
              <option value="hi">हिंदी (Hindi)</option>
            </select>
          </div>
        </header>

        {/* Messages Area */}
        <div className="max-w-4xl mx-auto px-4 py-6 h-[calc(100vh-200px)] overflow-y-auto">
          {messages.length === 0 ? (
            <div className="text-center py-20">
              <div className="w-20 h-20 bg-gradient-to-br from-orange-500 to-amber-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <BookOpen className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Welcome, Seeker
              </h2>
              <p className="text-gray-600 mb-4">
                Ask me anything about Sanatan Dharma scriptures
              </p>
              <div className="max-w-md mx-auto text-left bg-white rounded-lg p-4 shadow-sm">
                <p className="text-sm text-gray-700 mb-2 font-semibold">Example questions:</p>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• What does the Bhagavad Gita say about controlling the mind?</li>
                  <li>• How can I deal with stress according to Hindu philosophy?</li>
                  <li>• What is Karma Yoga?</li>
                  <li>• Tell me about the nature of the soul</li>
                </ul>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      message.role === 'user'
                        ? 'bg-orange-500 text-white'
                        : 'bg-white shadow-sm border border-orange-100'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.content}</p>

                    {message.citations && message.citations.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-orange-200">
                        <p className="text-sm font-semibold text-gray-700 mb-2">Citations:</p>
                        <div className="space-y-2">
                          {message.citations.map((citation, i) => (
                            <div key={i} className="text-sm bg-orange-50 rounded p-2">
                              <p className="font-semibold text-orange-900">{citation.reference}</p>
                              <p className="text-gray-700 text-xs mt-1">{citation.text}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    <p className="text-xs mt-2 opacity-70">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}

              {isProcessing && (
                <div className="flex justify-start">
                  <div className="bg-white shadow-sm border border-orange-100 rounded-lg p-4">
                    <Loader2 className="w-5 h-5 animate-spin text-orange-500" />
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-orange-200 shadow-lg">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <form onSubmit={handleTextSubmit} className="flex gap-2">
              <button
                type="button"
                onClick={isRecording ? stopRecording : startRecording}
                disabled={isProcessing}
                className={`p-3 rounded-full transition-all ${
                  isRecording
                    ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                    : 'bg-orange-500 hover:bg-orange-600'
                } text-white disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {isRecording ? (
                  <Volume2 className="w-6 h-6" />
                ) : (
                  <Mic className="w-6 h-6" />
                )}
              </button>

              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={language === 'hi' ? 'अपना प्रश्न यहाँ टाइप करें...' : 'Type your question here...'}
                disabled={isProcessing || isRecording}
                className="flex-1 px-4 py-3 border border-orange-300 rounded-full focus:ring-2 focus:ring-orange-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              />

              <button
                type="submit"
                disabled={isProcessing || isRecording || !input.trim()}
                className="p-3 bg-orange-500 hover:bg-orange-600 text-white rounded-full disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isProcessing ? (
                  <Loader2 className="w-6 h-6 animate-spin" />
                ) : (
                  <Send className="w-6 h-6" />
                )}
              </button>
            </form>

            {isRecording && (
              <p className="text-center text-sm text-red-600 mt-2 animate-pulse">
                Recording... Click mic to stop
              </p>
            )}
            {isPlaying && (
              <p className="text-center text-sm text-orange-600 mt-2">
                Playing audio response...
              </p>
            )}
          </div>
        </div>
      </main>
    </>
  );
}
