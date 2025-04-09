'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './Gallery.module.css';

const Gallery = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const response = await axios.get('<YOUR-API-Gateway-URL>/images');
        setImages(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching images:', error);
        setLoading(false);
      }
    };

    fetchImages();
  }, []);

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  return (
    <div className={styles.gallery}>
      {images.map((image) => (
        <div key={image.image_id} className={styles.imageCard}>
          <img
            src={image.thumbnail_url}
            alt="Gallery thumbnail"
            width={200}
            height={150}
            className={styles.thumbnail}
          />
          <p className={styles.date}>
            {new Date(image.uploaded_at).toLocaleDateString()}
          </p>
        </div>
      ))}
    </div>
  );
};

export default Gallery;

