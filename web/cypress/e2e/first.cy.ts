describe('empty spec', () => {
  it('passes', () => {
    cy.visit('https://www.google.com/')
    cy.get('#W0wltc > .QS5gu').click()
    cy.get('.gLFyf').type("recursion wikiped")
    cy.get('.gLFyf').type("{downarrow}{enter}")
    cy.get('.LC20lb').first().contains("Recursion")
  })
})
