import React from 'react';

const VideoDetails = ({ videoData, formData }) => {
  return (
    <div className="p-8 bg-white rounded-card shadow-strong">
      <h3 className="mb-6 text-2xl font-bold font-montserrat text-petroleo-500">
        Video Details
      </h3>
      <div className="space-y-4">
        <div className="p-4 rounded-button bg-humo-600">
          <span className="text-sm font-medium font-source text-petroleo-400">URL:</span>
          <p className="mt-1 text-sm break-all font-source text-petroleo-500">{videoData?.url}</p>
        </div>
        <div className="p-4 text-center rounded-button bg-coral-500/10">
          <div className="text-lg font-bold font-montserrat text-coral-500">
            Adidas
          </div>
          <div className="text-xs font-source text-petroleo-400">Target Brand</div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          {videoData?.views && (
            <div className="p-4 text-center rounded-button bg-mostaza-500/10">
              <div className="text-lg font-bold font-montserrat text-mostaza-500">
                {videoData.views.toLocaleString()}
              </div>
              <div className="text-xs font-source text-petroleo-400">Views</div>
            </div>
          )}
          {videoData?.comments && (
            <div className="p-4 text-center rounded-button bg-lila-500/10">
              <div className="text-lg font-bold font-montserrat text-lila-500">
                {videoData.comments.toLocaleString()}
              </div>
              <div className="text-xs font-source text-petroleo-400">Comments</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VideoDetails;