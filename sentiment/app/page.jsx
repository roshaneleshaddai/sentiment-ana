'use client'
import { useState } from "react";
import {toast, ToastContainer} from 'react-toastify';

export default function Home() {
  const [url, setUrl] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      toast.error(error.message, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      }
      );
    } finally {
      setLoading(false);
    }
  };
  const totalReviews = results.length;
  if(totalReviews !== 0){
    return (
      <div>No Data found</div>
    )
  }
  const positiveReviews = results.filter(result => result.Sentiment === "Positive").length;
  const negativeReviews = results.filter(result => result.Sentiment === "Negative").length;
  const neutralReviews = results.filter(result => result.Sentiment === "Neutral").length;
  const piracyMentions = results.filter(result => result["Piracy Mention"]).length;

  return (
    <div className="flex justify-center m-60">
      <div className="border-black border-2 text-center p-32">
        <ToastContainer />
        <h1 className="font-bold text-3xl">Sentiment Analysis Tool</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="p-4 m-4 border-black border-2 rounded-lg"
            required
          />
          <button type="submit" className="bg-blue-500 text-white p-4 rounded">
            Analyze
          </button>
        </form>
        {loading && <p>Loading...</p>}
        <div>
         
            <div className="mt-4 flex gap-10">
              <div className="flex flex-col">
              <p className="text-gray">Total Reviews</p>
              <strong>{totalReviews}</strong>
              </div>
              <div className="flex flex-col">
                <p className="text-gray">Positive Reviews</p>
                <strong>{positiveReviews}</strong>
              </div>
              <div className="flex flex-col">
                <p className="text-gray">Negative Reviews</p>
                <strong>{negativeReviews}</strong>
              </div>
              <div className="flex flex-col">
                <p className="text-gray">Neutral Reviews</p>
                <strong>{neutralReviews}</strong>
              </div>
              <div className="flex flex-col">
                <p className="text-gray">Piracy Mentions</p>
                <strong>{piracyMentions}</strong>
                </div>
              
            </div>
          {results.length > 0 && (
            <table className="border-2 border-black w-full mt-4">
              <thead>
                <tr className="border border-black">
                  <th className="border border-black p-2">Review</th>
                  <th className="border border-black p-2">Sentiment</th>
                  <th className="border border-black p-2">Piracy Mention</th>
                </tr>
              </thead>
              <tbody>
                {results.map((result, index) => (
                  <tr key={index} className="border border-black">
                    <td className="border border-black p-2">{result.Review}</td>
                    <td className="border border-black p-2">{result.Sentiment}</td>
                    <td className="border border-black p-2">
                      {result["Piracy Mention"] ? "Yes" : "No"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
