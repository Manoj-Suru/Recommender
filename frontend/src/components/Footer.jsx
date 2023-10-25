import React from 'react'

const Footer = () => {
  const currentYear = new Date().getFullYear();
  return (
    <footer>
        <p>© {currentYear} Movie Recommendations. All rights reserved.</p>
    </footer>
  )
}

export default Footer