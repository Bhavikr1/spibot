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

    const currentInput = input;
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);

    try {
      // Prepare conversation history (last 6 messages for context)
      const conversationHistory = messages.slice(-6).map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      // Use streaming endpoint
      const response = await fetch(`${API_URL}/api/text/query/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: currentInput,
          language: language,
          include_citations: true,
          conversation_history: conversationHistory
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch response');
      }

      // Create assistant message placeholder
      const assistantMessage: Message = {
        role: 'assistant',
        content: '',
        citations: [],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Read the streaming response with smooth animation
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (reader) {
        let accumulatedContent = '';
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;

          // Process complete lines
          const lines = buffer.split('\n');
          buffer = lines.pop() || ''; // Keep incomplete line in buffer

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const content = line.slice(6).trim();
              if (content && content !== '[DONE]' && !content.startsWith('[ERROR]')) {
                // Parse JSON-encoded content (backend escapes newlines for SSE)
                try {
                  const decoded = JSON.parse(content);
                  accumulatedContent += decoded;
                } catch {
                  // Fallback for non-JSON content
                  accumulatedContent += content;
                }

                // Update the last message with accumulated content - smooth update
                setMessages(prev => {
                  const newMessages = [...prev];
                  const lastMessage = newMessages[newMessages.length - 1];
                  if (lastMessage && lastMessage.role === 'assistant') {
                    lastMessage.content = accumulatedContent;
                  }
                  return newMessages;
                });

                // Small delay for smoother streaming effect
                await new Promise(resolve => setTimeout(resolve, 10));
              }
            }
          }
        }
      }
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
      // Step 1: Send audio for transcription only
      const formData = new FormData();
      formData.append('audio', audioBlob, 'query.wav');
      formData.append('language', language);

      // First, get transcription
      const transcribeResponse = await axios.post(`${API_URL}/api/voice/query`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob'
      });

      // Get transcription from headers
      const transcription = transcribeResponse.headers['x-transcription'] || 'Voice query';

      // Show user's transcribed message
      const userMessage: Message = {
        role: 'user',
        content: transcription,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, userMessage]);

      // Step 2: Use streaming endpoint to get bot response
      const conversationHistory = messages.slice(-6).map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      const streamResponse = await fetch(`${API_URL}/api/text/query/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: transcription,
          language: language,
          include_citations: true,
          conversation_history: conversationHistory
        }),
      });

      if (!streamResponse.ok) {
        throw new Error('Failed to fetch response');
      }

      // Create assistant message placeholder
      const assistantMessage: Message = {
        role: 'assistant',
        content: '',
        citations: [],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Read streaming response
      const reader = streamResponse.body?.getReader();
      const decoder = new TextDecoder();

      if (reader) {
        let accumulatedContent = '';
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;

          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const content = line.slice(6).trim();
              if (content && content !== '[DONE]' && !content.startsWith('[ERROR]')) {
                // Parse JSON-encoded content (backend escapes newlines for SSE)
                try {
                  const decoded = JSON.parse(content);
                  accumulatedContent += decoded;
                } catch {
                  // Fallback for non-JSON content
                  accumulatedContent += content;
                }

                setMessages(prev => {
                  const newMessages = [...prev];
                  const lastMessage = newMessages[newMessages.length - 1];
                  if (lastMessage && lastMessage.role === 'assistant') {
                    lastMessage.content = accumulatedContent;
                  }
                  return newMessages;
                });

                await new Promise(resolve => setTimeout(resolve, 10));
              }
            }
          }
        }
      }

      // Step 3: Play audio response
      const audioUrl = URL.createObjectURL(transcribeResponse.data);
      const audio = new Audio(audioUrl);

      setIsPlaying(true);
      audio.onended = () => setIsPlaying(false);
      await audio.play();

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
        <style>{`
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
          }
          .message-content {
            animation: fadeIn 0.3s ease-in;
            white-space: pre-line;
            line-height: 1.6;
          }
          .streaming-text {
            animation: fadeIn 0.2s ease-in;
            white-space: pre-line;
            line-height: 1.6;
          }
        `}</style>
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
                Welcome! I'm here to listen
              </h2>
              <p className="text-gray-600 mb-4 max-w-lg mx-auto">
                I'm your spiritual companion. Share what's on your mind - whether it's stress, confusion, or just curiosity about life's deeper questions. I'll listen, understand, and share wisdom from Sanatan Dharma that speaks to your situation.
              </p>
              <div className="max-w-md mx-auto text-left bg-white rounded-lg p-4 shadow-sm">
                <p className="text-sm text-gray-700 mb-2 font-semibold">You can simply say:</p>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• "I'm feeling really stressed lately"</li>
                  <li>• "I'm struggling with my relationships"</li>
                  <li>• "I feel lost and don't know my purpose"</li>
                  <li>• "I have trouble controlling my mind"</li>
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
                    <p className={`whitespace-pre-wrap ${isProcessing && index === messages.length - 1 ? 'streaming-text' : 'message-content'}`}>
                      {message.content || (isProcessing && index === messages.length - 1 ? '...' : '')}
                    </p>

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
