import { REPO } from '../content/index.js'

export default function Footer() {
  return (
    <footer className="footer">
      <p>
        <strong>Acknowledgments &amp; data credit.</strong> The data used in this project was provided by{' '}
        <a href="https://flyrank.ai" target="_blank" rel="noreferrer">FlyRank</a> (https://flyrank.ai) for the
        FlyRank Machine Learning Internship. Charts that identify individual clients are left out of this site.
      </p>
      <p>
        Source: <a href={REPO} target="_blank" rel="noreferrer">GitHub repository</a>. All figures are saved
        outputs of the notebooks linked on each page.
      </p>
    </footer>
  )
}
