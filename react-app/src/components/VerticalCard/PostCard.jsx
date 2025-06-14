import React from "react";
import "./PostCard.css";

const PostCard = ({ userName, dateTime, postContent, tags, image }) => {
  const renderContent = () => {
    if (typeof postContent === "string") {
      return <p>{postContent}</p>; // Render string content
    } else if (React.isValidElement(postContent)) {
      return <div>{postContent}</div>; // Render JSX content
    } else {
      return <p>Invalid content</p>; // Fallback for unexpected content types
    }
  };

  return (
    <div className="post-card">
      {/* User info */}
      <div className="post-card-header">
        <span className="user-name">{userName}</span>
        <span className="date-time">• {dateTime}</span>
      </div>

      {/* Post content */}
      <div className="post-card-body text-base text-gray-800">
        {renderContent()}
        {image && (
          <div className="max-w-xs mx-auto mt-2">
            <img
              src={image}
              alt="Post visual"
              className="h-20 w-20 object-cover rounded"
              style={{ maxWidth: '300px', maxHeight: '300px', borderRadius: '8%' }}
            />
          </div>
        )}
      </div>

      {/* Tags */}
      {tags && tags.length > 0 && (
        <div className="post-card-tags mt-4 flex flex-wrap gap-2">
          {tags.map((tag) => (
            <span key={tag} className="post-tag">
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

export default PostCard;