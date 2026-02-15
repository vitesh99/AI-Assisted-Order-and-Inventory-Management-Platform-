import React from 'react';

const MarkdownRenderer = ({ content }) => {
    if (!content) return null;

    // Split by newlines to handle blocks
    const lines = content.split('\n');

    return (
        <div className="text-gray-800 space-y-2">
            {lines.map((line, index) => {
                // Handle Lists (* item)
                if (line.trim().startsWith('* ')) {
                    const text = line.trim().substring(2);
                    return (
                        <div key={index} className="flex items-start">
                            <span className="mr-2 text-blue-500">•</span>
                            <span dangerouslySetInnerHTML={{ __html: parseBold(text) }} />
                        </div>
                    );
                }

                // Handle Headers or Bold-only lines slightly larger?
                // For now, just paragraph
                if (line.trim() === '') return <br key={index} />;

                return (
                    <p key={index} dangerouslySetInnerHTML={{ __html: parseBold(line) }} />
                );
            })}
        </div>
    );
};

// Helper to replace **text** with <strong>text</strong>
const parseBold = (text) => {
    // Escape HTML first to prevent XSS (basic)
    let safeText = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");

    // Replace **bold**
    return safeText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
};

export default MarkdownRenderer;
